from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import relationship

from app.models.base import Base, UUIDMixin


class CartStatus(str, PyEnum):
    open = "open"
    submitted = "submitted"


class PlanKind(str, PyEnum):
    economico = "economico"
    equilibrato = "equilibrato"
    un_solo_negozio = "un_solo_negozio"


class Cart(UUIDMixin, Base):
    __tablename__ = "cart"

    user_id = Column(ForeignKey("users.id"), nullable=False)
    status = Column(Enum(CartStatus), default=CartStatus.open, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="carts")
    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")
    plans = relationship("Plan", back_populates="cart")
    reservations = relationship("Reservation", back_populates="cart")


class CartItem(UUIDMixin, Base):
    __tablename__ = "cart_item"

    cart_id = Column(ForeignKey("cart.id"), nullable=False, index=True)
    product_id = Column(ForeignKey("product.id"), nullable=False)
    quantity = Column(Numeric, default=1)
    preferred_store_id = Column(ForeignKey("store.id"), nullable=True)
    notes = Column(Text, nullable=True)

    cart = relationship("Cart", back_populates="items")
    product = relationship("Product")
    preferred_store = relationship("Store")


class Plan(UUIDMixin, Base):
    __tablename__ = "plan"

    cart_id = Column(ForeignKey("cart.id"), nullable=False)
    kind = Column(Enum(PlanKind), nullable=False)
    total = Column(Numeric, nullable=False)
    stores_used = Column(Numeric, nullable=False)
    km_est = Column(Numeric, nullable=True)
    details_json = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    cart = relationship("Cart", back_populates="plans")
