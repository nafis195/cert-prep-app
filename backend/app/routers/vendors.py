from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/vendors", tags=["vendors"])


@router.get("/", response_model=List[schemas.VendorRead])
def list_vendors(db: Session = Depends(get_db)):
    return db.query(models.Vendor).all()

