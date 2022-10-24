from fastapi import HTTPException

from users.data.repositories.user_repository import UserRepository
from users.domain.dto.user import UserRegisterInSchema, UserCreateDBSchema
from users.utils.security import get_password_hash


class RegisterUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def __call__(self, new_user: UserRegisterInSchema) -> None:
        if await self.repository.email_exists(new_user.email):
            raise HTTPException(status_code=400, detail="User with this email already exists")
        await self.repository.create_user(
            data=UserCreateDBSchema(
                first_name=new_user.first_name,
                last_name=new_user.last_name,
                email=new_user.email,
                phone=new_user.phone,
                hashed_password=get_password_hash(new_user.password),
            )
        )
