from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from core.db.base_class import Base


class OutstandingToken(Base):
    __tablename__ = "outstanding_token"

    user_id = Column(Integer)

    jti = Column(String, unique=True, index=True, nullable=False)
    token = Column(String, nullable=False)

    expires_at = Column(DateTime(timezone=True))

    blacklist_token = relationship(
        "BlacklistToken", back_populates="outstanding_token", uselist=False
    )
