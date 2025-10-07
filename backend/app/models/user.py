from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import Boolean, Column, DateTime, Enum, String
from sqlalchemy.orm import relationship

from app.models.base import Base, UUIDMixin


class FulfillmentPref(str, PyEnum):
    in_negozio = "in_negozio"
    consegna = "consegna"


class UserRole(str, PyEnum):
    user = "user"
    merchant = "merchant"
    admin = "admin"


class User(UUIDMixin, Base):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=False)
    cap = Column(String, nullable=False)
    fulfillment_pref = Column(Enum(FulfillmentPref), default=FulfillmentPref.in_negozio, nullable=False)
    consent_geoloc = Column(Boolean, default=False, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    carts = relationship("Cart", back_populates="user")
    favorites = relationship("UserFavorite", back_populates="user")
