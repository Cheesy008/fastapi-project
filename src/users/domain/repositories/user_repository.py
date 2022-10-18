from typing import Protocol

from users.data.models import User


class IUserRepository(Protocol):
    model = User

    async def create_user(self, data: dict) -> None:
        ...

    async def email_exists(self, email: str) -> bool:
        ...

    async def get_by_email(self, email: str) -> User | None:
        ...

    async def get_by_id(self, user_id: int) -> User | None:
        ...
