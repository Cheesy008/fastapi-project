from fastapi import APIRouter

from users.api.endpoints import router as users_router


def include_routers() -> APIRouter:
    main_router = APIRouter()
    main_router.include_router(users_router, prefix="/users")
    return main_router
