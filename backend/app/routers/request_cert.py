from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..deps import get_current_user

router = APIRouter(prefix="/request-cert", tags=["certification-requests"])


@router.post("/", response_model=schemas.CertificationRequestRead)
def submit_certification_request(
    req_in: schemas.CertificationRequestCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    req = models.CertificationRequest(
        user_id=current_user.id,
        vendor_name=req_in.vendor_name,
        vendor_slug=req_in.vendor_slug,
        cert_name=req_in.cert_name,
        exam_code=req_in.exam_code,
        difficulty=req_in.difficulty,
        details=req_in.details,
        official_url=req_in.official_url,
    )
    db.add(req)
    db.commit()
    db.refresh(req)
    return req


@router.get("/me", response_model=List[schemas.CertificationRequestRead])
def list_my_requests(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return db.query(models.CertificationRequest).filter(models.CertificationRequest.user_id == current_user.id).all()

