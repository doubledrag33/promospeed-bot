from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import relationship

from app.models.base import Base, UUIDMixin


class ReservationStatus(str, PyEnum):
    sent = "sent"
    preparazione = "preparazione"
    pronto = "pronto"
    ritirato = "ritirato"
    annullato = "annullato"


class Reservation(UUIDMixin, Base):
    __tablename__ = "reservation"

    cart_id = Column(ForeignKey("cart.id"), nullable=False)
    store_id = Column(ForeignKey("store.id"), nullable=False)
    status = Column(Enum(ReservationStatus), default=ReservationStatus.sent, nullable=False)
    pickup_code = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    cart = relationship("Cart", back_populates="reservations")
    store = relationship("Store", back_populates="reservations")
