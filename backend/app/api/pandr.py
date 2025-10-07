import secrets

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_current_merchant, get_db
from app.models.cart import Cart
from app.models.reservation import Reservation, ReservationStatus
from app.models.store import Store

router = APIRouter()


@router.post("/pandr/create")
def create_reservation(payload: dict, db: Session = Depends(get_db), current_user=Depends(get_current_user)) -> dict:
    cart_id = payload.get("cart_id")
    store_ids = payload.get("store_ids") or []
    cart = db.query(Cart).filter(Cart.id == cart_id, Cart.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Carrello non trovato")

    if not store_ids:
        partner_store = (
            db.query(Store)
            .filter(Store.is_partner.is_(True))
            .order_by(Store.created_at)
            .first()
        )
        if not partner_store:
            raise HTTPException(status_code=400, detail="Nessun partner disponibile")
        store_ids = [partner_store.id]

    reservations = []
    for store_id in store_ids:
        store = db.query(Store).filter(Store.id == store_id, Store.is_partner.is_(True)).first()
        if not store:
            raise HTTPException(status_code=400, detail="Store non partner")
        reservation = Reservation(
            cart_id=cart.id,
            store_id=store.id,
            pickup_code=secrets.token_hex(3).upper(),
        )
        db.add(reservation)
        reservations.append(reservation)
    db.commit()
    return {"reservations": [str(res.id) for res in reservations]}


@router.get("/pandr/{reservation_id}")
def get_reservation(reservation_id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)) -> dict:
    reservation = (
        db.query(Reservation)
        .join(Cart)
        .filter(Reservation.id == reservation_id, Cart.user_id == current_user.id)
        .first()
    )
    if not reservation:
        raise HTTPException(status_code=404, detail="Prenotazione non trovata")
    return {
        "id": str(reservation.id),
        "status": reservation.status.value,
        "pickup_code": reservation.pickup_code,
    }


@router.patch("/pandr/{reservation_id}")
def update_reservation(
    reservation_id: str,
    payload: dict,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_merchant),
) -> dict:
    status_value = payload.get("status")
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Prenotazione non trovata")
    try:
        reservation.status = ReservationStatus(status_value)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Status non valido") from exc
    db.commit()
    return {"status": reservation.status.value}
