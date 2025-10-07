from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.models.cart import Cart, CartItem, CartStatus
from app.models.product import Product
from app.schemas.cart import (
    CartItemCreate,
    CartItemResponse,
    CartItemUpdate,
    CartResponse,
    OptimizeRequest,
    OptimizeResponse,
    PriceCompareRequest,
    PriceCompareResponse,
)
from app.services.optimize import generate_plans
from app.services.pricing import fetch_latest_prices

router = APIRouter()


def _get_or_create_cart(db: Session, user_id: str) -> Cart:
    cart = db.query(Cart).filter(Cart.user_id == user_id, Cart.status == CartStatus.open).first()
    if cart:
        return cart
    cart = Cart(user_id=user_id)
    db.add(cart)
    db.commit()
    db.refresh(cart)
    return cart


@router.get("/cart", response_model=CartResponse)
def get_cart(db: Session = Depends(get_db), current_user=Depends(get_current_user)) -> CartResponse:
    cart = _get_or_create_cart(db, str(current_user.id))
    return CartResponse.model_validate(cart)


@router.post("/cart/items", response_model=CartItemResponse)
def add_item(payload: CartItemCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)) -> CartItemResponse:
    cart = _get_or_create_cart(db, str(current_user.id))
    product = db.query(Product).filter(Product.id == payload.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Prodotto non trovato")
    item = CartItem(
        cart_id=cart.id,
        product_id=payload.product_id,
        quantity=payload.quantity,
        preferred_store_id=payload.preferred_store_id,
        notes=payload.notes,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return CartItemResponse.model_validate(item)


@router.patch("/cart/items/{item_id}", response_model=CartItemResponse)
def update_item(item_id: str, payload: CartItemUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)) -> CartItemResponse:
    cart = _get_or_create_cart(db, str(current_user.id))
    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item non trovato")
    if payload.quantity is not None:
        item.quantity = payload.quantity
    if payload.preferred_store_id is not None:
        item.preferred_store_id = payload.preferred_store_id
    if payload.notes is not None:
        item.notes = payload.notes
    db.commit()
    db.refresh(item)
    return CartItemResponse.model_validate(item)


@router.delete("/cart/items/{item_id}")
def delete_item(item_id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)) -> dict:
    cart = _get_or_create_cart(db, str(current_user.id))
    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item non trovato")
    db.delete(item)
    db.commit()
    return {"status": "deleted"}


@router.post("/list/price-compare", response_model=PriceCompareResponse)
def price_compare(payload: PriceCompareRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)) -> PriceCompareResponse:
    cart = db.query(Cart).filter(Cart.id == payload.cart_id, Cart.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Carrello non trovato")
    product_ids = [item.product_id for item in cart.items]
    price_map = fetch_latest_prices(db, product_ids)
    items = []
    for item in cart.items:
        snapshots = price_map.get(item.product_id, [])
        options = [
            {
                "store_id": str(snapshot.store.id),
                "store_name": snapshot.store.name,
                "price": snapshot.price.price,
                "unit_price": snapshot.price.unit_price,
                "source_type": snapshot.price.source_type,
                "source_ref": snapshot.price.source_ref,
                "captured_at": snapshot.price.captured_at.isoformat(),
            }
            for snapshot in snapshots
        ]
        items.append(
            {
                "product_id": item.product_id,
                "product_name": item.product.name if item.product else "",
                "options": options,
            }
        )
    return PriceCompareResponse(items=items)


@router.post("/list/optimize", response_model=OptimizeResponse)
def optimize(payload: OptimizeRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)) -> OptimizeResponse:
    cart = db.query(Cart).filter(Cart.id == payload.cart_id, Cart.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Carrello non trovato")
    plans = generate_plans(db, cart, payload.slider, payload.userLat, payload.userLon)
    serialized = [
        {
            "kind": plan.kind.value,
            "total": float(plan.total),
            "stores_used": plan.stores_used,
            "km_est": plan.km_est,
            "details": plan.details,
        }
        for plan in plans
    ]
    return OptimizeResponse(plans=serialized)
