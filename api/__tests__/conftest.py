import asyncio
import os
from typing import Generator

import alembic
from alembic.config import Config

from dependency_injector.wiring import Provide, inject

from httpx import AsyncClient

import pytest

from api import app
from api.containers import Container

from database import Sessionmaker


@pytest.fixture(scope="session")
def event_loop() -> asyncio.AbstractEventLoop:
    return asyncio.new_event_loop()


@pytest.fixture(scope="session", autouse=True)
def apply_migrations() -> Generator[None, None, None]:
    config = Config("alembic.ini")
    os.environ["TESTING"] = "1"
    alembic.command.upgrade(config, "head")
    yield
    alembic.command.downgrade(config, "base")
    os.environ["TESTING"] = "0"


@pytest.fixture(scope="session")
async def client() -> AsyncClient:
    return AsyncClient(app=app.app, base_url="http://test")


@pytest.fixture(scope="session")
@inject
def sessionmaker(
    maker: Sessionmaker = Provide[Container.db.sessionmaker],
) -> Sessionmaker:
    return maker
