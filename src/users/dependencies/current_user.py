from fastapi import Depends, Body, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, OAuth2PasswordBearer, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.db import get_session
from users.data.repositories.jwt_decoder_repository import JWTDecoderRepository
from users.data.repositories.user_repository import UserRepository
from users.domain.dto.user import UserSchema
from users.domain.use_cases.get_current_user_use_case import GetCurrentUserUseCase
from users.enums import TokenType

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/login/access-token")

auth_scheme = HTTPBearer()


async def get_current_user(
    session: AsyncSession = Depends(get_session),
    auth_credentials: HTTPAuthorizationCredentials = Depends(auth_scheme),
) -> UserSchema | None:
    token = JWTDecoderRepository.get_token_from_bearer_string(auth_credentials.credentials)
    get_current_user_use_case = GetCurrentUserUseCase(
        jwt_decoder_repository=JWTDecoderRepository(session=session, token=token),
        user_repository=UserRepository(session=session),
    )
    return await get_current_user_use_case(token_type=TokenType.ACCESS)


async def get_current_user_from_refresh_token(
    session: AsyncSession = Depends(get_session), refresh_token: str = Body(..., embed=True)
) -> UserSchema | None:
    get_current_user_use_case = GetCurrentUserUseCase(
        jwt_decoder_repository=JWTDecoderRepository(session=session, token=refresh_token),
        user_repository=UserRepository(session=session),
    )
    return await get_current_user_use_case(
        token_type=TokenType.REFRESH, add_token_to_blacklist=True
    )


async def get_current_authenticated_user(user: UserSchema | None = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
