from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.models.offer import Offer
from app.models.product import Product
from app.models.sku import SKU
from app.models.store import Store
from app.schemas.product import OfferInfo, PriceInfo, ProductDetail
from app.services.pricing import best_price_for_product, fetch_latest_prices

router = APIRouter()


def _price_to_schema(snapshot) -> Optional[PriceInfo]:
    if not snapshot:
        return None
    price = snapshot.price
    return PriceInfo(
        store_id=str(snapshot.store.id),
        store_name=snapshot.store.name,
        price=price.price,
        unit_price=price.unit_price,
        source_type=price.source_type,
        source_ref=price.source_ref,
        captured_at=price.captured_at,
    )


@router.get("/products")
def list_products(
    query: str | None = Query(default=None),
    category: str | None = Query(default=None),
    limit: int = Query(default=20, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> dict:
    q = db.query(Product)
    if query:
        q = q.filter(Product.name.ilike(f"%{query}%"))
    if category:
        q = q.filter(Product.category == category)
    products = q.offset(offset).limit(limit).all()
    price_map = fetch_latest_prices(db, [str(prod.id) for prod in products])
    payload = []
    for product in products:
        best = best_price_for_product(price_map.get(str(product.id), []))
        payload.append(
            {
                "id": str(product.id),
                "brand": product.brand,
                "name": product.name,
                "qty_value": str(product.qty_value) if product.qty_value else None,
                "qty_unit": product.qty_unit,
                "category": product.category,
                "img_url": product.img_url,
                "best_price": _price_to_schema(best).model_dump() if best else None,
            }
        )
    return {"items": payload, "count": len(payload)}


@router.get("/products/{product_id}", response_model=ProductDetail)
def get_product(product_id: str, db: Session = Depends(get_db)) -> ProductDetail:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Prodotto non trovato")

    prices = fetch_latest_prices(db, [product_id]).get(product_id, [])
    best = best_price_for_product(prices)

    offer_rows = (
        db.query(Offer, Store)
        .join(SKU, SKU.id == Offer.sku_id)
        .join(Store, Store.id == SKU.store_id)
        .filter(SKU.product_id == product_id)
        .all()
    )
    offers = [
        OfferInfo(
            store_id=str(store.id),
            store_name=store.name,
            promo_price=offer.promo_price,
            mechanics=offer.mechanics,
            start=datetime.combine(offer.start, datetime.min.time()),
            end=datetime.combine(offer.end, datetime.min.time()),
            notes=offer.notes,
        )
        for offer, store in offer_rows
    ]

    return ProductDetail(
        id=str(product.id),
        brand=product.brand,
        name=product.name,
        qty_value=product.qty_value,
        qty_unit=product.qty_unit,
        category=product.category,
        img_url=product.img_url,
        best_price=_price_to_schema(best),
        offers=offers,
    )
