from datetime import datetime

from pydantic import BaseModel

from users.enums import TokenType


class TokenPayloadSchema(BaseModel):
    token_type: TokenType
    jti: str
    user_id: int
    expires_at: datetime


class TokenResponseSchema(BaseModel):
    access_token: str
    refresh_token: str


class CreateOutstandingTokenSchema(BaseModel):
    jti: str
    user_id: int
    expires_at: datetime
    token: str
