from users.data.repositories.user_repository import UserRepository
from users.domain.dto.user import UserSchema
from users.utils.db_obj_to_dict import db_obj_to_dict


class GetUserCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def __call__(self, user_id: int) -> UserSchema | None:
        user = await self.user_repository.get_by_id(user_id=user_id)
        return UserSchema(**db_obj_to_dict(user)) if user is not None else None
