from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
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
def homepage(request: Request, db: Session = Depends(get_db)):
    vendor_list = db.query(models.Vendor).all()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "vendors": vendor_list},
    )


@app.get("/vendor/{vendor_id}", response_class=HTMLResponse)
def vendor_certifications_page(
    vendor_id: UUID,
    request: Request,
    db: Session = Depends(get_db),
):
    vendor = db.get(models.Vendor, vendor_id)
    if not vendor:
        return templates.TemplateResponse(
            "certifications_list.html",
            {"request": request, "vendor": None, "certifications": []},
            status_code=404,
        )
    return templates.TemplateResponse(
        "certifications_list.html",
        {
            "request": request,
            "vendor": vendor,
            "certifications": vendor.certifications,
        },
    )


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
    return templates.TemplateResponse(
        "certification_detail.html",
        {"request": request, "cert": cert, "avg_rating": avg_rating},
    )

