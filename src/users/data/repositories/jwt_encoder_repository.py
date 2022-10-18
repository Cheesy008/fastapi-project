from datetime import datetime, timedelta
from typing import TypedDict
from uuid import uuid4

from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import get_settings
from users.data.models import OutstandingToken
from users.domain.repositories.jwt_token_repository import IJWTEncoderRepository
from users.enums import TokenType

settings = get_settings()


class TokenDataDict(TypedDict, total=False):
    token_type: TokenType
    jti: str
    user_id: int
    exp: datetime


class JWTEncoderRepository(IJWTEncoderRepository):
    def __init__(self, session: AsyncSession, user_id: int):
        self.session = session
        self.user_id = user_id

    @property
    def token_data(self) -> TokenDataDict:
        exp = datetime.utcnow() + timedelta(minutes=self.lifetime)
        jti = uuid4().hex
        return TokenDataDict(user_id=self.user_id, token_type=self.token_type, exp=exp, jti=jti)

    def _encode_payload(self) -> str:
        encoded_jwt = jwt.encode(
            self.token_data, settings.app.secret_key, algorithm=settings.app.algorithm
        )
        return encoded_jwt

    async def _save_token_to_db(self, token: str):
        db_obj = OutstandingToken(
            user_id=self.token_data["user_id"],
            jti=self.token_data["jti"],
            expires_at=self.token_data["exp"],
            token=token,
        )
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)

    async def create_token(self) -> str:
        token = self._encode_payload()
        await self._save_token_to_db(token)
        return token


class AccessTokenRepository(JWTEncoderRepository):
    token_type = TokenType.ACCESS
    lifetime = settings.app.access_token_expires_minutes


class RefreshTokenRepository(JWTEncoderRepository):
    token_type = TokenType.REFRESH
    lifetime = settings.app.refresh_token_expires_minutes
