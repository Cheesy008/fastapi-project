from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from users.data.models import OutstandingToken, BlacklistToken
from users.domain.dto.token import TokenPayloadSchema, CreateOutstandingTokenSchema


class TokenRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_outstanding_token(self, data: CreateOutstandingTokenSchema) -> None:
        db_token = OutstandingToken(**data.dict())
        self.session.add(db_token)
        await self.session.commit()
        await self.session.refresh(db_token)

    async def find_outstanding_token(self, jti: str, user_id: int):
        outstanding_token = await self.session.execute(
            select(OutstandingToken).where(
                OutstandingToken.jti == jti,
                OutstandingToken.user_id == user_id,
            )
        )
        return outstanding_token.one_or_none()

    async def find_blacklist_token(self, jti: str, user_id: int):
        black_list_token = await self.session.execute(
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
        blacklist_token = BlacklistToken(outstanding_token=outstanding_token[0])
        self.session.add(blacklist_token)
        await self.session.commit()
        await self.session.refresh(blacklist_token)
