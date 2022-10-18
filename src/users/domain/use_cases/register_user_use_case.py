from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from users.domain.dto.user import UserRegisterInSchema, UserCreateDBSchema
from users.domain.repositories.user_repository import IUserRepository
from users.utils.security import get_password_hash


class RegisterUserUseCase:
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    def _prepare_obj_in_db(self, obj) -> dict:
        hashed_password = get_password_hash(obj.password)
        user_in_db = UserCreateDBSchema(
            email=obj.email,
            phone=obj.phone,
            hashed_password=hashed_password,
        )
        return jsonable_encoder(user_in_db)

    async def __call__(self, new_user: UserRegisterInSchema) -> None:
        if await self.repository.email_exists(new_user.email):
            raise HTTPException(status_code=400, detail="User with this email already exists")
        user_in_db = self._prepare_obj_in_db(new_user)
        await self.repository.create_user(user_in_db)
        # TODO добавить отправку на email
