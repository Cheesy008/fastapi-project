from typing import Callable

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from users.data.models import User
from users.domain.dto.user import UserCreateDBSchema, BaseUserSchema


class UserRepository:
    model = User

    def __init__(self, session_factory: Callable[..., AsyncSession]) -> None:
        self.session_factory = session_factory

    async def create_user(self, data: UserCreateDBSchema) -> None:
        async with self.session_factory() as session:
            db_user = self.model(**data.dict())
            session.add(db_user)
            await session.commit()

    async def update_user(self, data: BaseUserSchema, user_db: User) -> User:
        obj_data = jsonable_encoder(user_db)
        update_data = data.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(user_db, field, update_data[field])
        async with self.session_factory() as session:
            session.add(user_db)
            await session.commit()
            return user_db

    async def email_exists(self, email: str) -> bool:
        async with self.session_factory() as session:
            results = await session.execute(select(self.model).where(self.model.email == email))
            return bool(results.scalar())

    async def get_by_email(self, email: str) -> User | None:
        async with self.session_factory() as session:
            results = await session.execute(select(self.model).where(self.model.email == email))
            results = results.one_or_none()
            if not results:
                return None
            return results[0]

    async def get_by_id(self, user_id: int) -> User | None:
        async with self.session_factory() as session:
            results = await session.execute(select(self.model).where(self.model.id == user_id))
            results = results.one_or_none()
            if not results:
                return None
            return results[0]
