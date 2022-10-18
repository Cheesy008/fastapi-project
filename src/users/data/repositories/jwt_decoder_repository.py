from fastapi import HTTPException
from jose import jwt
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from users.domain.repositories.jwt_decoder_repository import IJWTDecoderRepository

from core.config import get_settings
from users.data.models import BlacklistToken, OutstandingToken
from users.domain.dto.token import TokenEncodedData
from users.enums import TokenType

settings = get_settings()


class JWTDecoderRepository(IJWTDecoderRepository):
    def __init__(self, session: AsyncSession, token: str):
        self.session = session
        self.token = token
        self.token_decoded_data = None

    @staticmethod
    def get_token_from_bearer_string(bearer_string: str):
        try:
            return bearer_string.split(" ")[1]
        except IndexError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid Bearer string",
            )

    def _decode(self) -> TokenEncodedData:
        try:
            payload = jwt.decode(
                self.token, settings.app.secret_key, algorithms=[settings.app.algorithm]
            )
            return TokenEncodedData(**payload)
        except (jwt.JWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
            )

    async def verify(self, token_data: TokenEncodedData):
        black_list_token = await self.session.execute(
            select(BlacklistToken)
            .join(OutstandingToken)
            .where(
                OutstandingToken.jti == token_data.jti,
                OutstandingToken.user_id == token_data.user_id,
            )
        )
        black_list_token = black_list_token.one_or_none()
        if black_list_token:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token in blacklist",
            )

    async def decode_token(
        self, token_type: TokenType, add_token_to_blacklist: bool = False
    ) -> TokenEncodedData:
        self.token_decoded_data = self._decode()
        await self.verify(self.token_decoded_data)
        if self.token_decoded_data.token_type != token_type:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Token type must be {token_type.title()}",
            )
        if add_token_to_blacklist:
            await self.add_to_blacklist()
        return self.token_decoded_data

    async def add_to_blacklist(self):
        outstanding_token = await self.session.execute(
            select(OutstandingToken).where(
                OutstandingToken.jti == self.token_decoded_data.jti,
                OutstandingToken.user_id == self.token_decoded_data.user_id,
            )
        )
        outstanding_token = outstanding_token.one_or_none()
        if not outstanding_token:
            outstanding_token = OutstandingToken(
                user_id=self.token_decoded_data.user_id,
                jti=self.token_decoded_data.jti,
                expires_at=self.token_decoded_data.exp,
                token=self.token,
            )
            self.session.add(outstanding_token)
            await self.session.commit()
            await self.session.refresh(outstanding_token)
        blacklist_token = BlacklistToken(outstanding_token=outstanding_token)
        self.session.add(blacklist_token)
        await self.session.commit()
        await self.session.refresh(blacklist_token)
