from fastapi import FastAPI, Depends, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from uuid import UUID

from .database import get_db
from . import models
from .routers import vendors, certifications, auth, ratings
from .routers.request_cert import router as request_cert_router
from .routers.admin import router as admin_router

app = FastAPI(title="Cert Prep App")

app.include_router(auth.router)
app.include_router(vendors.router)
app.include_router(certifications.router)
app.include_router(ratings.router)
app.include_router(request_cert_router)
app.include_router(admin_router)

app.mount("/static", StaticFiles(directory="backend/app/static"), name="static")
templates = Jinja2Templates(directory="backend/app/templates")


@app.get("/", response_class=HTMLResponse)
def homepage(
    request: Request,
    db: Session = Depends(get_db),
    q: str | None = Query(default=None),
    vendor_id: str | None = Query(default=None),
):
    # Difficulty label mapping for the UI badges.
    difficulty_labels = {
        "beginner": "Foundational",
        "intermediate": "Associate",
        "advanced": "Expert",
    }

    vendor_uuid = None
    if vendor_id:
        vendor_uuid = UUID(vendor_id)

    # Sidebar counts (for active/approved certs only).
    vendor_counts_rows = (
        db.query(models.Certification.vendor_id, func.count(models.Certification.id).label("cnt"))
        .filter(models.Certification.is_active.is_(True))
        .group_by(models.Certification.vendor_id)
        .all()
    )
    vendor_counts = {vid: int(cnt) for vid, cnt in vendor_counts_rows}

    vendors_list = db.query(models.Vendor).order_by(models.Vendor.name.asc()).all()

    # Certifications list with average rating + rating count.
    like = f"%{q}%" if q else None
    cert_rows = (
        db.query(
            models.Certification,
            models.Vendor.name.label("vendor_name"),
            func.coalesce(func.avg(models.Rating.rating), 0).label("avg_rating"),
            func.count(models.Rating.id).label("rating_count"),
        )
        .join(models.Vendor, models.Certification.vendor_id == models.Vendor.id)
        .outerjoin(models.Rating, models.Rating.certification_id == models.Certification.id)
        .filter(models.Certification.is_active.is_(True))
    )
    if vendor_uuid is not None:
        cert_rows = cert_rows.filter(models.Certification.vendor_id == vendor_uuid)
    if like:
        cert_rows = cert_rows.filter(
            or_(
                models.Certification.name.ilike(like),
                models.Certification.exam_code.ilike(like),
            )
        )

    cert_rows = cert_rows.group_by(models.Certification.id, models.Vendor.id, models.Vendor.name)
    cards = []
    for cert, vendor_name, avg_rating, rating_count in cert_rows.all():
        cards.append(
            {
                "cert": cert,
                "vendor_name": vendor_name,
                "avg_rating": float(avg_rating) if avg_rating is not None else None,
                "rating_count": int(rating_count) if rating_count is not None else 0,
            }
        )

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "vendors": vendors_list,
            "vendor_counts": vendor_counts,
            "active_vendor_id": vendor_id,
            "q": q,
            "cards": cards,
            "difficulty_labels": difficulty_labels,
        },
    )


@app.get("/vendor/{vendor_id}", response_class=HTMLResponse)
def vendor_certifications_page(
    vendor_id: UUID,
    request: Request,
    db: Session = Depends(get_db),
):
    # Keep old route working by redirecting to the new homepage grid.
    from fastapi.responses import RedirectResponse

    return RedirectResponse(url=f"/?vendor_id={vendor_id}")


@app.get("/certification/{cert_id}", response_class=HTMLResponse)
def certification_detail_page(
    cert_id: UUID,
    request: Request,
    db: Session = Depends(get_db),
):
    cert = db.get(models.Certification, cert_id)
    if not cert:
        return templates.TemplateResponse(
            "certification_detail.html",
            {"request": request, "cert": None},
            status_code=404,
        )
    scores = [r.rating for r in cert.ratings]
    avg_rating = sum(scores) / len(scores) if scores else None
    difficulty_labels = {
        "beginner": "Foundational",
        "intermediate": "Associate",
        "advanced": "Expert",
    }

    vendor_counts_rows = (
        db.query(models.Certification.vendor_id, func.count(models.Certification.id).label("cnt"))
        .filter(models.Certification.is_active.is_(True))
        .group_by(models.Certification.vendor_id)
        .all()
    )
    vendor_counts = {vid: int(cnt) for vid, cnt in vendor_counts_rows}
    vendors_list = db.query(models.Vendor).order_by(models.Vendor.name.asc()).all()

    return templates.TemplateResponse(
        "certification_detail.html",
        {
            "request": request,
            "cert": cert,
            "avg_rating": avg_rating,
            "difficulty_labels": difficulty_labels,
            "vendors": vendors_list,
            "vendor_counts": vendor_counts,
            "active_vendor_id": str(cert.vendor_id),
            "q": None,
        },
    )

