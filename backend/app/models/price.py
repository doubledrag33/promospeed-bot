from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import Column, Date, DateTime, Enum, ForeignKey, Integer, Numeric, Text
from sqlalchemy.orm import relationship

from app.models.base import Base, UUIDMixin


class PriceSource(str, PyEnum):
    volantino = "volantino"
    online = "online"
    scontrino = "scontrino"


class Price(UUIDMixin, Base):
    __tablename__ = "price"

    sku_id = Column(ForeignKey("sku.id"), nullable=False, index=True)
    price = Column(Numeric, nullable=False)
    unit_price = Column(Numeric, nullable=True)
    source_type = Column(Enum(PriceSource), nullable=False)
    source_ref = Column(Text, nullable=True)
    captured_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    valid_from = Column(Date, nullable=True)
    valid_to = Column(Date, nullable=True)
    confidence = Column(Integer, nullable=True)

    sku = relationship("SKU", back_populates="prices")
