from typing import Optional, Literal
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

DifficultyLevel = Literal["beginner", "intermediate", "advanced"]
RequestStatus = Literal["pending", "approved", "rejected"]


class VendorBase(BaseModel):
    name: str
    description: Optional[str] = None


class VendorCreate(VendorBase):
    slug: str


class VendorRead(BaseModel):
    id: UUID
    slug: str
    name: str
    description: Optional[str] = None

    class Config:
        orm_mode = True


class CertificationBase(BaseModel):
    vendor_id: UUID
    name: str
    exam_code: str
    difficulty: DifficultyLevel = "beginner"
    summary: Optional[str] = None
    description: Optional[str] = None
    official_url: Optional[str] = None
    is_active: bool = True


class CertificationRead(BaseModel):
    id: UUID
    vendor_id: UUID
    name: str
    exam_code: str
    difficulty: DifficultyLevel
    summary: Optional[str] = None
    description: Optional[str] = None
    official_url: Optional[str] = None
    is_active: bool

    average_rating: Optional[float] = None

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class UserRead(BaseModel):
    id: UUID
    email: EmailStr

    class Config:
        orm_mode = True


class RatingCreate(BaseModel):
    certification_id: UUID
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = None


class RatingRead(BaseModel):
    id: UUID
    user_id: UUID
    certification_id: UUID
    rating: int
    comment: Optional[str] = None

    class Config:
        orm_mode = True


class CertificationRequestCreate(BaseModel):
    vendor_name: str
    vendor_slug: Optional[str] = None
    cert_name: str
    exam_code: str
    difficulty: DifficultyLevel = "beginner"
    details: Optional[str] = None
    official_url: Optional[str] = None


class CertificationRequestRead(BaseModel):
    id: UUID
    user_id: UUID
    vendor_name: str
    vendor_slug: Optional[str] = None
    cert_name: str
    exam_code: str
    difficulty: DifficultyLevel
    details: Optional[str] = None
    official_url: Optional[str] = None
    status: RequestStatus
    reviewed_at: Optional[datetime] = None
    approved_by: Optional[UUID] = None
    rejected_by: Optional[UUID] = None
    admin_notes: Optional[str] = None

    class Config:
        orm_mode = True


class AdminReviewRequest(BaseModel):
    admin_notes: Optional[str] = None

