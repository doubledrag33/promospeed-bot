from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship

from app.models.base import Base, UUIDMixin


class ReceiptStatus(str, PyEnum):
    uploaded = "uploaded"
    parsed = "parsed"
    error = "error"


class Receipt(UUIDMixin, Base):
    __tablename__ = "receipt"

    user_id = Column(ForeignKey("users.id"), nullable=False)
    store_id = Column(ForeignKey("store.id"), nullable=False)
    img_url = Column(Text, nullable=False)
    ocr_json = Column(JSON, nullable=True)
    parsed_at = Column(DateTime, nullable=True)
    status = Column(Enum(ReceiptStatus), default=ReceiptStatus.uploaded, nullable=False)

    user = relationship("User")
    store = relationship("Store")
