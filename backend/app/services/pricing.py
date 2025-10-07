from collections import defaultdict
from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.price import Price
from app.models.product import Product
from app.models.sku import SKU
from app.models.store import Store


class ProductPriceSnapshot:
    def __init__(self, product: Product, store: Store, price: Price) -> None:
        self.product = product
        self.store = store
        self.price = price


def fetch_latest_prices(db: Session, product_ids: List[str]) -> Dict[str, List[ProductPriceSnapshot]]:
    results: Dict[str, List[ProductPriceSnapshot]] = defaultdict(list)
    if not product_ids:
        return results

    subquery = (
        db.query(Price.sku_id, func.max(Price.captured_at).label("max_captured"))
        .join(SKU, Price.sku_id == SKU.id)
        .filter(SKU.product_id.in_(product_ids))
        .group_by(Price.sku_id)
        .subquery()
    )

    rows = (
        db.query(Product, Store, Price)
        .join(SKU, SKU.product_id == Product.id)
        .join(Store, Store.id == SKU.store_id)
        .join(Price, Price.sku_id == SKU.id)
        .join(subquery, (subquery.c.sku_id == Price.sku_id) & (subquery.c.max_captured == Price.captured_at))
        .filter(Product.id.in_(product_ids))
        .all()
    )

    for product, store, price in rows:
        results[str(product.id)].append(ProductPriceSnapshot(product, store, price))
    return results


def best_price_for_product(prices: List[ProductPriceSnapshot]) -> Optional[ProductPriceSnapshot]:
    if not prices:
        return None
    return min(prices, key=lambda item: Decimal(item.price.price))
