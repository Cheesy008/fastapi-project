from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Body, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, OAuth2PasswordBearer, HTTPBearer

from users.domain.dto.user import UserOutSchema
from users.domain.use_cases import DecodeTokenCase, GetUserCase
from users.enums import TokenType
from users.utils.auth import get_token_from_bearer_string

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/login/access-token")

auth_scheme = HTTPBearer()


@inject
async def get_current_user(
    auth_credentials: HTTPAuthorizationCredentials = Depends(auth_scheme),
    decode_token_uc: DecodeTokenCase = Depends(Provide["use_cases.decode_token_uc"]),
    get_user_uc: GetUserCase = Depends(Provide["use_cases.get_user_uc"]),
) -> UserOutSchema | None:
    token = get_token_from_bearer_string(bearer_string=auth_credentials.credentials)
    decoded_token = await decode_token_uc(token=token, token_type=TokenType.ACCESS)
    return await get_user_uc(user_id=decoded_token.user_id)


@inject
async def get_current_user_from_refresh_token(
    refresh_token: str = Body(..., embed=True),
    decode_token_uc: DecodeTokenCase = Depends(Provide["use_cases.decode_token_uc"]),
    get_user_uc: GetUserCase = Depends(Provide["use_cases.get_user_uc"]),
) -> UserOutSchema | None:
    decoded_token = await decode_token_uc(
        token=refresh_token, token_type=TokenType.REFRESH, add_token_to_blacklist=True
    )
    return await get_user_uc(user_id=decoded_token.user_id)


async def get_current_authenticated_user(user: UserOutSchema | None = Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
