from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, UniqueConstraint

from app.models.base import Base, UUIDMixin


class UserFavorite(UUIDMixin, Base):
    __tablename__ = "user_favorite"
    __table_args__ = (UniqueConstraint("user_id", "product_id", name="uq_user_product"),)

    user_id = Column(ForeignKey("users.id"), nullable=False)
    product_id = Column(ForeignKey("product.id"), nullable=False)
    rank = Column(Integer, nullable=True)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="favorites")
    product = relationship("Product", back_populates="favorites")


class StoreUser(UUIDMixin, Base):
    __tablename__ = "store_user"

    store_id = Column(ForeignKey("store.id"), nullable=False)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    role = Column(String, nullable=False)
