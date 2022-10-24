from fastapi import Depends, Body, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, OAuth2PasswordBearer, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.db import get_session
from users.data.repositories.token_repository import TokenRepository
from users.data.repositories.user_repository import UserRepository
from users.domain.dto.user import UserSchema
from users.domain.use_cases.decode_token_use_case import DecodeTokenCase
from users.domain.use_cases.get_user_use_case import GetUserCase
from users.enums import TokenType
from users.utils.auth import get_token_from_bearer_string

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/login/access-token")

auth_scheme = HTTPBearer()


async def get_current_user(
    session: AsyncSession = Depends(get_session),
    auth_credentials: HTTPAuthorizationCredentials = Depends(auth_scheme),
) -> UserSchema | None:
    token = get_token_from_bearer_string(bearer_string=auth_credentials.credentials)
    decode_token_case = DecodeTokenCase(repository=TokenRepository(session=session))
    decoded_token = await decode_token_case(token=token, token_type=TokenType.ACCESS)
    get_current_user_use_case = GetUserCase(user_repository=UserRepository(session=session))
    return await get_current_user_use_case(user_id=decoded_token.user_id)


async def get_current_user_from_refresh_token(
    session: AsyncSession = Depends(get_session), refresh_token: str = Body(..., embed=True)
) -> UserSchema | None:
    decode_token_case = DecodeTokenCase(repository=TokenRepository(session=session))
    decoded_token = await decode_token_case(
        token=refresh_token, token_type=TokenType.REFRESH, add_token_to_blacklist=True
    )
    get_current_user_use_case = GetUserCase(user_repository=UserRepository(session=session))
    return await get_current_user_use_case(user_id=decoded_token.user_id)


async def get_current_authenticated_user(user: UserSchema | None = Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
