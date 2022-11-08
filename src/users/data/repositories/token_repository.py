from typing import Callable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from users.data.models import OutstandingToken, BlacklistToken
from users.domain.dto.token import TokenPayloadSchema, CreateOutstandingTokenSchema


class TokenRepository:
    def __init__(self, session_factory: Callable[..., AsyncSession]):
        self.session_factory = session_factory

    async def create_outstanding_token(self, data: CreateOutstandingTokenSchema) -> None:
        db_token = OutstandingToken(**data.dict())
        async with self.session_factory() as session:
            session.add(db_token)
            await session.commit()

    async def find_outstanding_token(self, jti: str, user_id: int):
        async with self.session_factory() as session:
            outstanding_token = await session.execute(
                select(OutstandingToken).where(
                    OutstandingToken.jti == jti,
                    OutstandingToken.user_id == user_id,
                )
            )
            return outstanding_token.one_or_none()

    async def find_blacklist_token(self, jti: str, user_id: int):
        async with self.session_factory() as session:
            black_list_token = await session.execute(
                select(BlacklistToken)
                .join(OutstandingToken)
                .where(OutstandingToken.jti == jti, OutstandingToken.user_id == user_id)
            )
            return black_list_token.one_or_none()

    async def create_blacklist_token(self, data: TokenPayloadSchema, token: str):
        outstanding_token = await self.find_outstanding_token(jti=data.jti, user_id=data.user_id)
        if not outstanding_token:
            data_dict = data.dict()
            data_dict.pop("token_type")
            outstanding_token = await self.create_outstanding_token(
                data=CreateOutstandingTokenSchema(**data_dict, token=token)
            )
        async with self.session_factory() as session:
            blacklist_token = BlacklistToken(outstanding_token=outstanding_token[0])
            session.add(blacklist_token)
            await session.commit()
