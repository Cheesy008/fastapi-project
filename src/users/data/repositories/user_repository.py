from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from users.data.models import User
from users.domain.repositories.user_repository import IUserRepository


class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_user(self, data: dict) -> None:
        db_user = self.model(**data)
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)

    async def email_exists(self, email: str) -> bool:
        results = await self.session.execute(select(self.model).where(self.model.email == email))
        return bool(results.scalar())

    async def get_by_email(self, email: str) -> User | None:
        results = await self.session.execute(select(self.model).where(self.model.email == email))
        results = results.one_or_none()
        if not results:
            return None
        return results[0]

    async def get_by_id(self, user_id: int) -> User | None:
        results = await self.session.execute(select(self.model).where(self.model.id == user_id))
        results = results.one_or_none()
        if not results:
            return None
        return results[0]
