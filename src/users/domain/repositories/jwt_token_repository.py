from typing import Protocol

from users.enums import TokenType


class IJWTEncoderRepository(Protocol):
    token_type: TokenType
    lifetime: int

    async def create_token(self) -> str:
        ...
