from typing import Optional, List

from pydantic import BaseModel, EmailStr


class VendorBase(BaseModel):
    name: str
    description: Optional[str] = None


class VendorCreate(VendorBase):
    pass


class VendorRead(VendorBase):
    id: int

    class Config:
        orm_mode = True


class CertificationBase(BaseModel):
    vendor_id: int
    name: str
    exam_code: str
    level: Optional[str] = None
    short_description: Optional[str] = None
    full_description: Optional[str] = None


class CertificationCreate(CertificationBase):
    pass


class CertificationRead(CertificationBase):
    id: int
    average_rating: Optional[float] = None

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


class RatingBase(BaseModel):
    certification_id: int
    score: int
    comment: Optional[str] = None


class RatingCreate(RatingBase):
    pass


class RatingRead(RatingBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

