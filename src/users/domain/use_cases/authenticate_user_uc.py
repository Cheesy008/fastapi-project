from users.data.repositories.user_repository import UserRepository
from users.domain.dto.user import UserOutSchema
from users.utils.db_obj_to_dict import db_obj_to_dict
from users.utils.security import verify_password


class AuthenticateUserCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def __call__(self, email: str, password: str) -> UserOutSchema | None:
        user_db = await self.repository.get_by_email(email)
        if not user_db or not verify_password(password, user_db.hashed_password):
            return None
        return UserOutSchema(**db_obj_to_dict(user_db))
