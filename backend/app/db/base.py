from app.db.session import engine
from app.models import user, store, product, sku, price, offer, cart, reservation, receipt, favorite

__all__ = [
    "user",
    "store",
    "product",
    "sku",
    "price",
    "offer",
    "cart",
    "reservation",
    "receipt",
    "favorite",
]


def init_db() -> None:
    from app.models.base import Base

    Base.metadata.create_all(bind=engine)
