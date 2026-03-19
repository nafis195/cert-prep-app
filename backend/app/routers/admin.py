import re
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..deps import get_current_user

router = APIRouter(prefix="/admin", tags=["admin"])


def slugify(s: str) -> str:
    s = (s or "").strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
    return s or "vendor"


def require_admin(db: Session, current_user: models.User) -> None:
    admin_role = (
        db.query(models.UserRole)
        .filter(models.UserRole.user_id == current_user.id, models.UserRole.role == "admin")
        .first()
    )
    if not admin_role:
        raise HTTPException(status_code=403, detail="Admin privileges required")


@router.get("/requests", response_model=List[schemas.CertificationRequestRead])
def list_requests(
    status: Optional[schemas.RequestStatus] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    require_admin(db, current_user)
    query = db.query(models.CertificationRequest)
    if status is not None:
        query = query.filter(models.CertificationRequest.status == status)
    return query.order_by(models.CertificationRequest.created_at.desc()).all()


@router.post("/requests/{request_id}/approve", response_model=schemas.CertificationRequestRead)
def approve_request(
    request_id: UUID,
    body: schemas.AdminReviewRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    require_admin(db, current_user)

    req = db.get(models.CertificationRequest, request_id)
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    if req.status != "pending":
        raise HTTPException(status_code=400, detail=f"Request is already {req.status}")

    vendor_slug = req.vendor_slug or slugify(req.vendor_name)

    vendor = db.query(models.Vendor).filter(models.Vendor.slug == vendor_slug).first()
    if not vendor:
        vendor = models.Vendor(slug=vendor_slug, name=req.vendor_name, description=None)
        db.add(vendor)
        db.flush()  # obtain vendor.id without commit

    certification = (
        db.query(models.Certification)
        .filter(models.Certification.vendor_id == vendor.id, models.Certification.exam_code == req.exam_code)
        .first()
    )

    if not certification:
        certification = models.Certification(
            vendor_id=vendor.id,
            name=req.cert_name,
            exam_code=req.exam_code,
            difficulty=req.difficulty,
            summary=None,
            description=req.details,
            official_url=req.official_url,
            is_active=True,
        )
        db.add(certification)
        db.flush()
    else:
        certification.name = req.cert_name
        certification.difficulty = req.difficulty
        certification.description = req.details
        certification.official_url = req.official_url
        certification.is_active = True

    req.status = "approved"
    req.reviewed_at = datetime.utcnow()
    req.approved_by = current_user.id
    req.admin_notes = body.admin_notes

    db.commit()
    db.refresh(req)
    return req


@router.post("/requests/{request_id}/reject", response_model=schemas.CertificationRequestRead)
def reject_request(
    request_id: UUID,
    body: schemas.AdminReviewRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    require_admin(db, current_user)

    req = db.get(models.CertificationRequest, request_id)
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    if req.status != "pending":
        raise HTTPException(status_code=400, detail=f"Request is already {req.status}")

    req.status = "rejected"
    req.reviewed_at = datetime.utcnow()
    req.rejected_by = current_user.id
    req.admin_notes = body.admin_notes

    db.commit()
    db.refresh(req)
    return req

