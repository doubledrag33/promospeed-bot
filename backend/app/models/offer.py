from sqlalchemy import Column, Date, ForeignKey, Numeric, Text
from sqlalchemy.orm import relationship

from app.models.base import Base, UUIDMixin


class Offer(UUIDMixin, Base):
    __tablename__ = "offer"

    sku_id = Column(ForeignKey("sku.id"), nullable=False, index=True)
    promo_price = Column(Numeric, nullable=False)
    mechanics = Column(Text, nullable=True)
    start = Column(Date, nullable=False)
    end = Column(Date, nullable=False)
    notes = Column(Text, nullable=True)

    sku = relationship("SKU", back_populates="offers")
