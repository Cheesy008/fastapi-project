from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.db import get_session
from users.data.repositories.user_repository import UserRepository
from users.dependencies.current_user import get_current_authenticated_user
from users.domain.dto.user import UserRegisterInSchema, UserSchema
from users.domain.use_cases import RegisterUserUseCase

router = APIRouter()


@router.post("/register")
async def register_user_route(
    user: UserRegisterInSchema, session: AsyncSession = Depends(get_session)
):
    use_case = RegisterUserUseCase(repository=UserRepository(session=session))
    await use_case(user)
    return Response(status_code=200)


@router.get("/me", response_model=UserSchema)
def get_current_user_route(user: UserSchema = Depends(get_current_authenticated_user)):
    return user
