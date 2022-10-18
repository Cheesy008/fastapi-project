from sqlalchemy import Column, String, Boolean, DateTime, func, Float, Enum

from core.db.base_class import Base
from users.enums import BustType


class User(Base):
    __tablename__ = "user"

    # first_name = Column(String, nullable=False)
    # last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    phone = Column(String, nullable=False)
    birth_date = Column(DateTime(timezone=True), nullable=True)
    avatar = Column(String(), unique=True, nullable=True)
    uae_id = Column(String(100), nullable=True)
    passport_id = Column(String(100), nullable=True)
    street = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    instagram_url = Column(String(), nullable=True)
    height = Column(Float(), nullable=True)
    weight = Column(Float(), nullable=True)
    zip_code = Column(String(100), nullable=True)
    bust_type = Column(Enum(BustType), nullable=True)
