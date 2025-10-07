from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_merchant, get_db
from app.models.reservation import Reservation
from app.schemas.cart import PlanDetailsItem

router = APIRouter()


@router.get("/orders")
def list_orders(db: Session = Depends(get_db), current_user=Depends(get_current_merchant)) -> dict:
    reservations = db.query(Reservation).filter(Reservation.store.has(is_partner=True)).all()
    return {
        "items": [
            {
                "id": str(res.id),
                "status": res.status.value,
                "pickup_code": res.pickup_code,
            }
            for res in reservations
        ]
    }
