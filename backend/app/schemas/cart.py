from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel


class CartItemCreate(BaseModel):
    product_id: str
    quantity: Decimal
    preferred_store_id: Optional[str] = None
    notes: Optional[str] = None


class CartItemUpdate(BaseModel):
    quantity: Optional[Decimal] = None
    preferred_store_id: Optional[str] = None
    notes: Optional[str] = None


class CartItemResponse(BaseModel):
    id: str
    product_id: str
    quantity: Decimal
    preferred_store_id: Optional[str]
    notes: Optional[str]

    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    id: str
    status: str
    items: List[CartItemResponse]

    class Config:
        from_attributes = True


class PriceCompareRequest(BaseModel):
    cart_id: str


class StorePriceBreakdown(BaseModel):
    store_id: str
    store_name: str
    price: Decimal
    unit_price: Optional[Decimal]
    source_type: str
    source_ref: Optional[str]
    captured_at: str


class ItemPriceComparison(BaseModel):
    product_id: str
    product_name: str
    options: List[StorePriceBreakdown]


class PriceCompareResponse(BaseModel):
    items: List[ItemPriceComparison]


class OptimizeRequest(BaseModel):
    cart_id: str
    userLat: Optional[float]
    userLon: Optional[float]
    slider: int = 5


class PlanDetailsItem(BaseModel):
    product_id: str
    product_name: str
    quantity: Decimal
    price: Decimal


class PlanStoreDetails(BaseModel):
    store_id: str
    store_name: str
    subtotal: Decimal
    items: List[PlanDetailsItem]


class OptimizePlan(BaseModel):
    kind: str
    total: Decimal
    stores_used: int
    km_est: Optional[float]
    details: List[PlanStoreDetails]


class OptimizeResponse(BaseModel):
    plans: List[OptimizePlan]
