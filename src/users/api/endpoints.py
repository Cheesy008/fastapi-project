from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Response, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from users.dependencies.current_user import (
    get_current_user_from_refresh_token,
    get_current_authenticated_user,
)
from users.domain.dto.token import TokenResponseSchema
from users.domain.dto.user import UserRegisterInSchema, UserOutSchema, BaseUserSchema
from users.domain.use_cases import (
    RegisterUserCase,
    AuthenticateUserCase,
    CreateAccessTokenCase,
    CreateRefreshTokenCase,
    UpdateUserCase,
)

router = APIRouter()


@router.post("/register")
@inject
async def register_user_route(
    user: UserRegisterInSchema,
    use_case: RegisterUserCase = Depends(Provide["use_cases.register_user_uc"]),
):
    await use_case(user)
    return Response(status_code=200)


@router.post("/login/access-token", response_model=TokenResponseSchema)
@inject
async def login_access_token_route(
    form_data: OAuth2PasswordRequestForm = Depends(),
    authenticate_user_uc: AuthenticateUserCase = Depends(Provide["use_cases.authenticate_user_uc"]),
    create_access_token_uc: CreateAccessTokenCase = Depends(
        Provide["use_cases.create_access_token_uc"]
    ),
    create_refresh_token_uc: CreateRefreshTokenCase = Depends(
        Provide["use_cases.create_refresh_token_uc"]
    ),
):
    user = await authenticate_user_uc(email=form_data.username, password=form_data.password)
    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token = await create_access_token_uc(user_id=user.id)
    refresh_token = await create_refresh_token_uc(user_id=user.id)
    return TokenResponseSchema(access_token=access_token, refresh_token=refresh_token)


@router.post("/login/refresh-token", response_model=TokenResponseSchema)
@inject
async def login_refresh_token_route(
    user: UserOutSchema = Depends(get_current_user_from_refresh_token),
    create_access_token_uc: CreateAccessTokenCase = Depends(
        Provide["use_cases.create_access_token_uc"]
    ),
    create_refresh_token_uc: CreateRefreshTokenCase = Depends(
        Provide["use_cases.create_refresh_token_uc"]
    ),
):
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    access_token = await create_access_token_uc(user_id=user.id)
    refresh_token = await create_refresh_token_uc(user_id=user.id)
    return TokenResponseSchema(access_token=access_token, refresh_token=refresh_token)


@router.get("/me", response_model=UserOutSchema)
async def get_current_user_route(user: UserOutSchema = Depends(get_current_authenticated_user)):
    return user


@router.patch("/me", response_model=UserOutSchema)
@inject
async def update_user_route(
    update_user: BaseUserSchema,
    user: UserOutSchema = Depends(get_current_authenticated_user),
    update_user_uc: UpdateUserCase = Depends(Provide["use_cases.update_user_uc"]),
):
    return await update_user_uc(update_user_schema=update_user, user_id=user.id)
