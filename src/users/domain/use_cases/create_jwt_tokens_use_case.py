from users.domain.repositories.jwt_token_repository import IJWTEncoderRepository


class CreateJWTTokenUseCase:
    def __init__(self, repository: IJWTEncoderRepository):
        self.repository = repository

    async def __call__(self) -> str:
        return await self.repository.create_token()
