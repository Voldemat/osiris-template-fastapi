import sys

from fastapi import FastAPI

import config

from .containers import Container
from .routers import base_router


class FastAPIWithContainer(FastAPI):
    container: Container


def create_app() -> FastAPIWithContainer:
    container = Container()
    container.config.from_dict(
        {
            "db": {
                "host": config.POSTGRES_HOST,
                "port": config.POSTGRES_PORT,
                "user": config.POSTGRES_USER,
                "password": config.POSTGRES_PASSWORD,
                "db": config.POSTGRES_DB,
            },
        }
    )
    app = FastAPIWithContainer(
        root_path=config.ROOT_PATH,
        title="Bootstrap FastAPI App",
        version="0.0.1",
    )
    app.container = container
    if "pytest" in sys.modules:
        container.wire(modules=[".__tests__.conftest"])

    app.include_router(base_router, tags=["Base"], prefix="/base")
    return app


app = create_app()
