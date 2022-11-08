from users.data.repositories.user_repository import UserRepository
from users.domain.dto.user import UserOutSchema
from users.utils.db_obj_to_dict import db_obj_to_dict


class GetUserCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def __call__(self, user_id: int) -> UserOutSchema | None:
        user = await self.repository.get_by_id(user_id=user_id)
        return UserOutSchema(**db_obj_to_dict(user)) if user is not None else None
