from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel


class PriceInfo(BaseModel):
    store_id: str
    store_name: str
    price: Decimal
    unit_price: Optional[Decimal]
    source_type: str
    source_ref: Optional[str]
    captured_at: datetime


class OfferInfo(BaseModel):
    store_id: str
    store_name: str
    promo_price: Decimal
    mechanics: Optional[str]
    start: datetime
    end: datetime
    notes: Optional[str]


class ProductBase(BaseModel):
    id: str
    brand: str
    name: str
    qty_value: Optional[Decimal]
    qty_unit: Optional[str]
    category: str
    img_url: Optional[str]

    class Config:
        from_attributes = True


class ProductDetail(ProductBase):
    best_price: Optional[PriceInfo]
    offers: List[OfferInfo] = []
