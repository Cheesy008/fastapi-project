from sqlalchemy import Column, String, Boolean, DateTime, func

from core.db.base_class import Base


class User(Base):
    __tablename__ = "user"

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    phone = Column(String, nullable=False)
    birth_date = Column(DateTime(timezone=True), nullable=True)
    street = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
