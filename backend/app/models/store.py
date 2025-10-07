from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Float, JSON, String, Text
from sqlalchemy.orm import relationship

from app.models.base import Base, UUIDMixin


class Store(UUIDMixin, Base):
    __tablename__ = "store"

    name = Column(String, nullable=False)
    chain = Column(String, nullable=False)
    address = Column(String, nullable=False)
    cap = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    hours_json = Column(JSON, nullable=True)
    has_everli = Column(Boolean, default=False, nullable=False)
    everli_deeplink = Column(Text, nullable=True)
    is_partner = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    skus = relationship("SKU", back_populates="store")
    reservations = relationship("Reservation", back_populates="store")
