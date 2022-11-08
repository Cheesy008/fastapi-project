from fastapi import FastAPI

from containers.container import Container
from core.config import get_settings
from users.api.router import include_routers


def create_app() -> FastAPI:
    settings = get_settings()
    container = Container()
    container.gateways.db()
    app = FastAPI(title=settings.app.name, debug=settings.app.debug)
    app.include_router(include_routers())
    app.container = container
    return app


app = create_app()
