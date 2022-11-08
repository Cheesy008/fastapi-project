from fastapi import HTTPException

from users.data.models import User
from users.data.repositories.user_repository import UserRepository
from users.domain.dto.user import BaseUserSchema


class UpdateUserCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def __call__(self, update_user_schema: BaseUserSchema, user_id: int) -> User:
        user_db = await self.repository.get_by_id(user_id=user_id)
        if user_db is None:
            raise HTTPException(status_code=404, detail="User not found")
        return await self.repository.update_user(data=update_user_schema, user_db=user_db)
