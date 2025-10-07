from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.models.favorite import UserFavorite
from app.models.product import Product

router = APIRouter()


@router.get("/favorites")
def list_favorites(db: Session = Depends(get_db), current_user=Depends(get_current_user)) -> dict:
    favorites = db.query(UserFavorite).filter(UserFavorite.user_id == current_user.id).all()
    return {
        "items": [
            {
                "id": str(fav.id),
                "product_id": str(fav.product_id),
                "notes": fav.notes,
            }
            for fav in favorites
        ]
    }


@router.post("/favorites")
def add_favorite(payload: dict, db: Session = Depends(get_db), current_user=Depends(get_current_user)) -> dict:
    product_id = payload.get("product_id")
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Prodotto non trovato")
    favorite = UserFavorite(user_id=current_user.id, product_id=product_id)
    db.add(favorite)
    db.commit()
    db.refresh(favorite)
    return {"id": str(favorite.id)}


@router.delete("/favorites/{favorite_id}")
def delete_favorite(favorite_id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)) -> dict:
    favorite = db.query(UserFavorite).filter(UserFavorite.id == favorite_id, UserFavorite.user_id == current_user.id).first()
    if not favorite:
        raise HTTPException(status_code=404, detail="Preferito non trovato")
    db.delete(favorite)
    db.commit()
    return {"status": "deleted"}
