from fastapi import HTTPException, status
from jose import jwt
from pydantic import ValidationError

from core.config import get_settings
from users.data.repositories.token_repository import TokenRepository
from users.domain.dto.token import TokenPayloadSchema
from users.enums import TokenType

settings = get_settings()


class DecodeTokenCase:
    def __init__(self, repository: TokenRepository):
        self.repository = repository

    async def __call__(
        self, token: str, token_type: TokenType, add_token_to_blacklist: bool = False
    ):
        try:
            payload = jwt.decode(
                token, settings.app.secret_key, algorithms=[settings.app.algorithm]
            )
            payload["expires_at"] = payload.pop("exp")
            token_decoded_data = TokenPayloadSchema(**payload)
        except (jwt.JWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
            )
        if (
            await self.repository.find_blacklist_token(
                jti=token_decoded_data.jti, user_id=token_decoded_data.user_id
            )
            is not None
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token in blacklist",
            )
        if token_decoded_data.token_type != token_type:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Token type must be {token_type.title()}",
            )
        if add_token_to_blacklist:
            await self.repository.create_blacklist_token(data=token_decoded_data, token=token)
        return token_decoded_data
