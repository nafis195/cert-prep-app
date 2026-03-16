from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..deps import get_current_user

router = APIRouter(prefix="/ratings", tags=["ratings"])


@router.post("/", response_model=schemas.RatingRead, status_code=status.HTTP_201_CREATED)
def create_or_update_rating(
    rating_in: schemas.RatingCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    cert = db.get(models.Certification, rating_in.certification_id)
    if not cert:
        raise HTTPException(status_code=404, detail="Certification not found")

    rating = (
        db.query(models.Rating)
        .filter(
            models.Rating.user_id == current_user.id,
            models.Rating.certification_id == rating_in.certification_id,
        )
        .first()
    )
    if not rating:
        rating = models.Rating(
            user_id=current_user.id,
            certification_id=rating_in.certification_id,
            score=rating_in.score,
            comment=rating_in.comment,
        )
        db.add(rating)
    else:
        rating.score = rating_in.score
        rating.comment = rating_in.comment

    db.commit()
    db.refresh(rating)
    return rating

