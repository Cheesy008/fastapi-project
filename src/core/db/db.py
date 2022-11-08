from contextlib import asynccontextmanager
from typing import Callable

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


class Database:
    def __init__(self, db_url: str) -> None:
        self._engine = create_async_engine(db_url, echo=True, future=True)

    @asynccontextmanager
    async def get_session(self) -> Callable[..., AsyncSession]:
        async_session = sessionmaker(self._engine, class_=AsyncSession, expire_on_commit=False)
        async with async_session() as session, session.begin():
            yield session
