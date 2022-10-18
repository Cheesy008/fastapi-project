from fastapi import FastAPI

from core.config import get_settings
from users.api.router import include_routers


def create_app() -> FastAPI:
    settings = get_settings()
    application = FastAPI(title=settings.app.name, debug=settings.app.debug)
    application.include_router(include_routers())
    return application


app = create_app()
