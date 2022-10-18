from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from core.db.base_class import Base


class BlacklistToken(Base):
    __tablename__ = "blacklist_token"

    outstanding_token_id = Column(Integer, ForeignKey("outstanding_token.id"))
    outstanding_token = relationship("OutstandingToken", back_populates="blacklist_token")
