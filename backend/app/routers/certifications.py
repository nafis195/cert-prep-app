from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/certifications", tags=["certifications"])


@router.get("/", response_model=List[schemas.CertificationRead])
def list_certifications(
    vendor_id: Optional[int] = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(
        models.Certification,
        func.coalesce(func.avg(models.Rating.score), 0).label("avg_rating"),
    ).outerjoin(models.Rating).group_by(models.Certification.id)

    if vendor_id is not None:
        query = query.filter(models.Certification.vendor_id == vendor_id)

    rows = query.all()
    result: List[schemas.CertificationRead] = []
    for cert, avg_rating in rows:
        item = schemas.CertificationRead.from_orm(cert)
        item.average_rating = float(avg_rating) if avg_rating is not None else None
        result.append(item)
    return result


@router.get("/{cert_id}", response_model=schemas.CertificationRead)
def get_certification(cert_id: int, db: Session = Depends(get_db)):
    row = (
        db.query(
            models.Certification,
            func.coalesce(func.avg(models.Rating.score), 0).label("avg_rating"),
        )
        .outerjoin(models.Rating)
        .filter(models.Certification.id == cert_id)
        .group_by(models.Certification.id)
        .first()
    )
    if not row:
        raise HTTPException(status_code=404, detail="Certification not found")
    cert, avg_rating = row
    item = schemas.CertificationRead.from_orm(cert)
    item.average_rating = float(avg_rating) if avg_rating is not None else None
    return item

