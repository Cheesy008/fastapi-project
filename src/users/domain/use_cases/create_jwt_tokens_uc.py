import functools
from datetime import datetime, timedelta
from typing import TypedDict
from uuid import uuid4

from jose import jwt

from core.config import get_settings
from users.data.repositories.token_repository import TokenRepository
from users.domain.dto.token import CreateOutstandingTokenSchema
from users.enums import TokenType

settings = get_settings()


class TokenDataDict(TypedDict):
    token_type: TokenType
    jti: str
    user_id: int
    exp: datetime


class CreateJWTToken:
    token_type: TokenType
    lifetime: int

    def __init__(self, repository: TokenRepository):
        self.repository = repository
        self.user_id = None

    @functools.cached_property
    def token_data(self) -> TokenDataDict:
        exp = datetime.utcnow() + timedelta(minutes=self.lifetime)
        jti = uuid4().hex
        return TokenDataDict(user_id=self.user_id, token_type=self.token_type, exp=exp, jti=jti)

    def _encode_payload(self) -> str:
        encoded_jwt = jwt.encode(
            self.token_data, settings.app.secret_key, algorithm=settings.app.algorithm
        )
        return encoded_jwt

    async def __call__(self, user_id: int) -> str:
        self.user_id = user_id
        token = self._encode_payload()
        await self.repository.create_outstanding_token(
            data=CreateOutstandingTokenSchema(
                user_id=user_id,
                jti=self.token_data["jti"],
                expires_at=self.token_data["exp"],
                token=token,
            )
        )
        return token


class CreateAccessTokenCase(CreateJWTToken):
    token_type = TokenType.ACCESS
    lifetime = settings.app.access_token_expires_minutes


class CreateRefreshTokenCase(CreateJWTToken):
    token_type = TokenType.REFRESH
    lifetime = settings.app.refresh_token_expires_minutes
