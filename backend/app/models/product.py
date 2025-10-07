from sqlalchemy import Column, JSON, Numeric, String, Text
from sqlalchemy.orm import relationship

from app.models.base import Base, UUIDMixin


class Product(UUIDMixin, Base):
    __tablename__ = "product"

    ean = Column(String, index=True)
    alt_codes = Column(JSON, default=list)
    brand = Column(String, nullable=False)
    name = Column(String, nullable=False)
    qty_value = Column(Numeric, nullable=True)
    qty_unit = Column(String, nullable=True)
    category = Column(String, nullable=False)
    img_url = Column(Text, nullable=True)

    skus = relationship("SKU", back_populates="product")
    favorites = relationship("UserFavorite", back_populates="product")
