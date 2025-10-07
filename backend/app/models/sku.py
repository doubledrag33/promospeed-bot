from sqlalchemy import Boolean, Column, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base, UUIDMixin


class SKU(UUIDMixin, Base):
    __tablename__ = "sku"

    product_id = Column(ForeignKey("product.id"), nullable=False)
    store_id = Column(ForeignKey("store.id"), nullable=False)
    is_private_label = Column(Boolean, default=False, nullable=False)

    product = relationship("Product", back_populates="skus")
    store = relationship("Store", back_populates="skus")
    prices = relationship("Price", back_populates="sku")
    offers = relationship("Offer", back_populates="sku")
