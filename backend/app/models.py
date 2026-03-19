from sqlalchemy import Column, Text, ForeignKey, UniqueConstraint, Boolean, String, DateTime, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text
from sqlalchemy.dialects.postgresql import UUID as PGUUID, ENUM as PGEnum

from .database import Base


DifficultyLevel = PGEnum(
    "beginner",
    "intermediate",
    "advanced",
    name="difficulty_level",
    schema="public",
    create_type=False,
)

RequestStatus = PGEnum(
    "pending",
    "approved",
    "rejected",
    name="request_status",
    schema="public",
    create_type=False,
)

AppRole = PGEnum(
    "user",
    "admin",
    name="app_role",
    schema="public",
    create_type=False,
)


class Vendor(Base):
    __tablename__ = "vendors"
    __table_args__ = {"schema": "public"}

    id = Column(PGUUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    slug = Column(String(200), unique=True, nullable=False)
    name = Column(String(200), unique=True, nullable=False)
    description = Column(Text)

    certifications = relationship("Certification", back_populates="vendor")


class Certification(Base):
    __tablename__ = "certifications"
    __table_args__ = {"schema": "public"}

    id = Column(PGUUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    vendor_id = Column(PGUUID(as_uuid=True), ForeignKey("public.vendors.id", ondelete="RESTRICT"), nullable=False)

    name = Column(String(250), nullable=False)
    exam_code = Column(String(100), nullable=False)
    difficulty = Column(DifficultyLevel, nullable=False, server_default=text("'beginner'::difficulty_level"))

    summary = Column(Text)
    description = Column(Text)
    official_url = Column(Text)
    is_active = Column(Boolean, nullable=False, server_default=text("true"))

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False)

    vendor = relationship("Vendor", back_populates="certifications")
    ratings = relationship("Rating", back_populates="certification")


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "public"}

    id = Column(PGUUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)

    profile = relationship("Profile", back_populates="user", uselist=False)
    roles = relationship("UserRole", back_populates="user")
    ratings = relationship("Rating", back_populates="user")


class Profile(Base):
    __tablename__ = "profiles"
    __table_args__ = {"schema": "public"}

    id = Column(PGUUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    user_id = Column(PGUUID(as_uuid=True), ForeignKey("public.users.id", ondelete="CASCADE"), unique=True, nullable=False)

    full_name = Column(String(250), nullable=False)
    avatar_url = Column(Text)

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False)

    user = relationship("User", back_populates="profile")
    ratings = relationship("Rating", back_populates="user")


class UserRole(Base):
    __tablename__ = "user_roles"

    id = Column(PGUUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    user_id = Column(PGUUID(as_uuid=True), ForeignKey("public.users.id", ondelete="CASCADE"), nullable=False)
    role = Column(AppRole, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "role", name="user_roles_user_id_role_key"),
        {"schema": "public"},
    )

    user = relationship("User", back_populates="roles")


class Rating(Base):
    __tablename__ = "ratings"
    __table_args__ = (
        UniqueConstraint("user_id", "certification_id", name="uq_user_cert_rating"),
        {"schema": "public"},
    )

    id = Column(PGUUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    user_id = Column(PGUUID(as_uuid=True), ForeignKey("public.users.id", ondelete="CASCADE"), nullable=False)
    certification_id = Column(PGUUID(as_uuid=True), ForeignKey("public.certifications.id", ondelete="CASCADE"), nullable=False)

    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False)

    user = relationship("User", back_populates="ratings")
    certification = relationship("Certification", back_populates="ratings")


class CertificationRequest(Base):
    __tablename__ = "certification_requests"
    __table_args__ = {"schema": "public"}

    id = Column(PGUUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    user_id = Column(PGUUID(as_uuid=True), ForeignKey("public.users.id", ondelete="CASCADE"), nullable=False)

    vendor_name = Column(Text, nullable=False)
    vendor_slug = Column(Text)
    cert_name = Column(Text, nullable=False)
    exam_code = Column(Text, nullable=False)
    difficulty = Column(DifficultyLevel, nullable=False, server_default=text("'beginner'::difficulty_level"))
    details = Column(Text)
    official_url = Column(Text)

    status = Column(RequestStatus, nullable=False, server_default=text("'pending'::request_status"))

    reviewed_at = Column(DateTime(timezone=True))
    approved_by = Column(PGUUID(as_uuid=True), ForeignKey("public.users.id"), nullable=True)
    rejected_by = Column(PGUUID(as_uuid=True), ForeignKey("public.users.id"), nullable=True)
    admin_notes = Column(Text)

    created_at = Column(DateTime(timezone=True), nullable=False)

