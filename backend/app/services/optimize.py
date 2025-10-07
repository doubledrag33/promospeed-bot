from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal
from typing import Dict, Iterable, List, Optional

from haversine import haversine
from sqlalchemy.orm import Session

from app.models.cart import Cart, PlanKind
from app.models.price import Price
from app.models.product import Product
from app.models.sku import SKU
from app.models.store import Store


@dataclass
class Candidate:
    product: Product
    store: Store
    price: Decimal


@dataclass
class PlanResult:
    kind: PlanKind
    total: Decimal
    stores_used: int
    km_est: Optional[float]
    details: List[dict]


def _load_candidates(db: Session, cart: Cart) -> Dict[str, List[Candidate]]:
    product_ids = [item.product_id for item in cart.items]
    if not product_ids:
        return {}

    rows = (
        db.query(Product, Store, Price)
        .join(SKU, SKU.product_id == Product.id)
        .join(Store, Store.id == SKU.store_id)
        .join(Price, Price.sku_id == SKU.id)
        .filter(Product.id.in_(product_ids))
        .order_by(Price.captured_at.desc())
        .all()
    )
    candidates: Dict[str, List[Candidate]] = defaultdict(list)
    for product, store, price in rows:
        candidates[str(product.id)].append(
            Candidate(product=product, store=store, price=Decimal(price.price))
        )
    return candidates


def _economical_plan(candidates: Dict[str, List[Candidate]], cart: Cart) -> PlanResult:
    totals: Dict[str, Decimal] = defaultdict(lambda: Decimal("0"))
    items_by_store: Dict[str, List[dict]] = defaultdict(list)
    store_map: Dict[str, Store] = {}
    for item in cart.items:
        options = candidates.get(item.product_id, [])
        if not options:
            continue
        best = min(options, key=lambda c: c.price)
        subtotal = best.price * Decimal(item.quantity)
        store_map[str(best.store.id)] = best.store
        totals[str(best.store.id)] += subtotal
        items_by_store[str(best.store.id)].append(
            {
                "product_id": str(best.product.id),
                "product_name": best.product.name,
                "quantity": str(item.quantity),
                "price": str(best.price),
            }
        )
    details = [
        {
            "store": {"id": store_id, "name": store_map[store_id].name},
            "subtotal": str(total),
            "items": items_by_store[store_id],
        }
        for store_id, total in totals.items()
    ]
    return PlanResult(PlanKind.economico, sum(totals.values(), Decimal("0")), len(totals), None, details)


def _equilibrato_plan(candidates: Dict[str, List[Candidate]], cart: Cart, slider: int) -> PlanResult:
    lambda1 = Decimal("2.0") * (Decimal("0.5") + Decimal(slider) / Decimal("20"))
    totals: Dict[str, Decimal] = defaultdict(lambda: Decimal("0"))
    items_by_store: Dict[str, List[dict]] = defaultdict(list)
    store_map: Dict[str, Store] = {}
    open_stores: set[str] = set()

    for item in cart.items:
        options = candidates.get(item.product_id, [])
        if not options:
            continue
        best_option = None
        best_cost = Decimal("Infinity")
        for candidate in options:
            subtotal = candidate.price * Decimal(item.quantity)
            penalty = Decimal("0") if str(candidate.store.id) in open_stores else lambda1
            cost = subtotal + penalty
            if cost < best_cost:
                best_cost = cost
                best_option = candidate
        if best_option:
            store_id = str(best_option.store.id)
            if store_id not in open_stores:
                open_stores.add(store_id)
            store_map[store_id] = best_option.store
            totals[store_id] += best_option.price * Decimal(item.quantity)
            items_by_store[store_id].append(
                {
                    "product_id": str(best_option.product.id),
                    "product_name": best_option.product.name,
                    "quantity": str(item.quantity),
                    "price": str(best_option.price),
                }
            )

    details = [
        {
            "store": {"id": store_id, "name": store_map[store_id].name},
            "subtotal": str(total),
            "items": items_by_store[store_id],
        }
        for store_id, total in totals.items()
    ]
    return PlanResult(PlanKind.equilibrato, sum(totals.values(), Decimal("0")), len(totals), None, details)


def _single_store_plan(candidates: Dict[str, List[Candidate]], cart: Cart) -> PlanResult:
    totals_by_store: Dict[str, Decimal] = defaultdict(lambda: Decimal("0"))
    for item in cart.items:
        options = candidates.get(item.product_id, [])
        for candidate in options:
            totals_by_store[str(candidate.store.id)] += candidate.price * Decimal(item.quantity)
    if not totals_by_store:
        return PlanResult(PlanKind.un_solo_negozio, Decimal("0"), 0, None, [])
    best_store_id = min(totals_by_store, key=totals_by_store.get)
    total = totals_by_store[best_store_id]
    items = []
    store_name = ""
    for item in cart.items:
        options = [c for c in candidates.get(item.product_id, []) if str(c.store.id) == best_store_id]
        if not options:
            continue
        candidate = min(options, key=lambda c: c.price)
        store_name = candidate.store.name
        items.append(
            {
                "product_id": str(candidate.product.id),
                "product_name": candidate.product.name,
                "quantity": str(item.quantity),
                "price": str(candidate.price),
            }
        )
    details = [
        {
            "store": {"id": best_store_id, "name": store_name},
            "subtotal": str(total),
            "items": items,
        }
    ]
    return PlanResult(PlanKind.un_solo_negozio, total, 1 if items else 0, None, details)


def _estimate_distance(user_coords: Optional[tuple[float, float]], stores: Iterable[Store]) -> Optional[float]:
    if not user_coords:
        return None
    stores_list = list(stores)
    if not stores_list:
        return None
    distances = [haversine(user_coords, (store.lat, store.lon)) for store in stores_list]
    if not distances:
        return None
    return float(sum(distances) / len(distances))


def generate_plans(db: Session, cart: Cart, slider: int, user_lat: Optional[float], user_lon: Optional[float]) -> List[PlanResult]:
    candidates = _load_candidates(db, cart)
    plans = []
    user_coords = (user_lat, user_lon) if user_lat is not None and user_lon is not None else None

    economical = _economical_plan(candidates, cart)
    economical.km_est = _estimate_distance(user_coords, _stores_from_details(candidates, economical))
    plans.append(economical)

    equilibrato = _equilibrato_plan(candidates, cart, slider)
    equilibrato.km_est = _estimate_distance(user_coords, _stores_from_details(candidates, equilibrato))
    plans.append(equilibrato)

    single = _single_store_plan(candidates, cart)
    single.km_est = _estimate_distance(user_coords, _stores_from_details(candidates, single))
    plans.append(single)

    return plans


def _stores_from_details(candidates: Dict[str, List[Candidate]], plan: PlanResult) -> List[Store]:
    store_ids = {detail["store"]["id"] for detail in plan.details if detail.get("store")}
    stores: Dict[str, Store] = {}
    for options in candidates.values():
        for candidate in options:
            stores[str(candidate.store.id)] = candidate.store
    return [stores[sid] for sid in store_ids if sid in stores]
