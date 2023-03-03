from functools import cache
from typing import AsyncGenerator

from dependency_injector.wiring import Provide, inject

from sqlalchemy.ext.asyncio import AsyncSession

from database import Sessionmaker

from ..containers import Container


@cache
@inject
def get_sessionmaker(
    maker: Sessionmaker = Provide[Container.db.sessionmaker],
) -> Sessionmaker:
    return maker


async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with get_sessionmaker()() as session:
        yield session
