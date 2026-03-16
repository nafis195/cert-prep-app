from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, UniqueConstraint
from sqlalchemy.orm import relationship

from .database import Base


class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)

    certifications = relationship("Certification", back_populates="vendor")


class Certification(Base):
    __tablename__ = "certifications"

    id = Column(Integer, primary_key=True, index=True)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    name = Column(String(150), nullable=False)
    exam_code = Column(String(50), nullable=False)
    level = Column(String(50), nullable=True)
    short_description = Column(Text, nullable=True)
    full_description = Column(Text, nullable=True)

    vendor = relationship("Vendor", back_populates="certifications")
    ratings = relationship("Rating", back_populates="certification")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    ratings = relationship("Rating", back_populates="user")


class Rating(Base):
    __tablename__ = "ratings"
    __table_args__ = (
        UniqueConstraint("user_id", "certification_id", name="uq_user_cert_rating"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    certification_id = Column(Integer, ForeignKey("certifications.id"), nullable=False)
    score = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)

    user = relationship("User", back_populates="ratings")
    certification = relationship("Certification", back_populates="ratings")

