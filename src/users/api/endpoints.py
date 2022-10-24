from fastapi import APIRouter, Depends, Response, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.db import get_session
from users.data.repositories.token_repository import TokenRepository
from users.data.repositories.user_repository import UserRepository
from users.dependencies.current_user import (
    get_current_authenticated_user,
    get_current_user_from_refresh_token,
)
from users.domain.dto.token import TokenResponseSchema
from users.domain.dto.user import UserRegisterInSchema, UserSchema
from users.domain.use_cases import RegisterUserUseCase
from users.domain.use_cases.authenticate_user_use_case import AuthenticateUserCase
from users.domain.use_cases.create_jwt_tokens_use_case import (
    CreateAccessTokenCase,
    CreateRefreshTokenCase,
)

router = APIRouter()


@router.post("/register")
async def register_user_route(
    user: UserRegisterInSchema, session: AsyncSession = Depends(get_session)
):
    use_case = RegisterUserUseCase(repository=UserRepository(session=session))
    await use_case(user)
    return Response(status_code=200)


@router.post("/login/access-token", response_model=TokenResponseSchema)
async def login_access_token_route(
    session: AsyncSession = Depends(get_session), form_data: OAuth2PasswordRequestForm = Depends()
):
    authenticate_use_case = AuthenticateUserCase(repository=UserRepository(session=session))
    user = await authenticate_use_case(email=form_data.username, password=form_data.password)
    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    repository = TokenRepository(session=session)
    access_use_case = CreateAccessTokenCase(repository=repository)
    access_token = await access_use_case(user_id=user.id)
    refresh_use_case = CreateRefreshTokenCase(repository=repository)
    refresh_token = await refresh_use_case(user_id=user.id)
    return TokenResponseSchema(access_token=access_token, refresh_token=refresh_token)


@router.post("/login/refresh-token", response_model=TokenResponseSchema)
async def login_refresh_token_route(
    session: AsyncSession = Depends(get_session),
    user: UserSchema = Depends(get_current_user_from_refresh_token),
):
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    repository = TokenRepository(session=session)
    access_use_case = CreateAccessTokenCase(repository=repository)
    access_token = await access_use_case(user_id=user.id)
    refresh_use_case = CreateRefreshTokenCase(repository=repository)
    refresh_token = await refresh_use_case(user_id=user.id)
    return TokenResponseSchema(access_token=access_token, refresh_token=refresh_token)


@router.get("/me", response_model=UserSchema)
def get_current_user_route(user: UserSchema = Depends(get_current_authenticated_user)):
    return user
