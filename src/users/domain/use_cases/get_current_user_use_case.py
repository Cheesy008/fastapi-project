from users.domain.dto.user import UserSchema
from users.domain.repositories.user_repository import IUserRepository
from users.enums import TokenType
from users.utils.db_obj_to_dict import db_obj_to_dict


class GetCurrentUserUseCase:
    def __init__(self, jwt_decoder_repository, user_repository: IUserRepository):
        self.jwt_decoder_repository = jwt_decoder_repository
        self.user_repository = user_repository

    async def __call__(
        self, token_type: TokenType, add_token_to_blacklist: bool = False
    ) -> UserSchema | None:
        token_data = await self.jwt_decoder_repository.decode_token(
            token_type, add_token_to_blacklist=add_token_to_blacklist
        )
        user = await self.user_repository.get_by_id(user_id=token_data.user_id)
        if not user:
            return None
        return UserSchema(**db_obj_to_dict(user))
