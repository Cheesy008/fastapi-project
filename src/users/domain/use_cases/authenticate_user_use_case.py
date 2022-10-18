from users.domain.dto.user import UserSchema
from users.domain.repositories import IUserRepository
from users.utils.db_obj_to_dict import db_obj_to_dict
from users.utils.security import verify_password


class AuthenticateUserUseCase:
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    async def __call__(self, email: str, password: str) -> UserSchema | None:
        user_db = await self.repository.get_by_email(email)
        if not user_db or not verify_password(password, user_db.hashed_password):
            return None
        return UserSchema(**db_obj_to_dict(user_db))
