from typing import Protocol

from users.domain.dto.token import TokenEncodedData
from users.enums import TokenType


class IJWTDecoderRepository(Protocol):
    @staticmethod
    def get_token_from_bearer_string(bearer_string: str):
        ...

    async def verify(self, token_data: TokenEncodedData):
        ...

    async def decode_token(
        self,
        token_type: TokenType,
        add_token_to_blacklist: bool = False,
    ) -> TokenEncodedData:
        ...

    async def add_to_blacklist(self):
        ...
