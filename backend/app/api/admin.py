from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin, get_db
from app.models.store import Store

router = APIRouter()


@router.get("/stores")
def list_stores(db: Session = Depends(get_db), current_user=Depends(get_current_admin)) -> dict:
    stores = db.query(Store).all()
    return {
        "items": [
            {
                "id": str(store.id),
                "name": store.name,
                "is_partner": store.is_partner,
            }
            for store in stores
        ]
    }


@router.post("/stores")
def create_store(payload: dict, db: Session = Depends(get_db), current_user=Depends(get_current_admin)) -> dict:
    store = Store(
        name=payload["name"],
        chain=payload.get("chain", ""),
        address=payload.get("address", ""),
        cap=payload.get("cap", ""),
        lat=payload.get("lat", 0.0),
        lon=payload.get("lon", 0.0),
        is_partner=payload.get("is_partner", False),
    )
    db.add(store)
    db.commit()
    db.refresh(store)
    return {"id": str(store.id)}


@router.patch("/stores/{store_id}")
def update_store(store_id: str, payload: dict, db: Session = Depends(get_db), current_user=Depends(get_current_admin)) -> dict:
    store = db.query(Store).filter(Store.id == store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store non trovato")
    for field in ["name", "chain", "address", "cap", "lat", "lon", "is_partner", "has_everli", "everli_deeplink"]:
        if field in payload:
            setattr(store, field, payload[field])
    db.commit()
    return {"status": "updated"}
