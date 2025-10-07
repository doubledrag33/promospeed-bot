from typing import Optional

from sqlalchemy.orm import Session

from app.models.product import Product


def resolve_code(db: Session, code: str) -> Optional[Product]:
    product = db.query(Product).filter(Product.ean == code).first()
    if product:
        return product
    return db.query(Product).filter(Product.alt_codes.contains([code])).first()
