import contextlib
from typing import (
    AsyncContextManager,
    AsyncGenerator,
    Callable,
    TypeVar,
)

import pytest

import sqlalchemy as sa

from database import Sessionmaker
from database.models import BaseModel


ModelType = TypeVar("ModelType", bound=BaseModel)

InstanceContextManager = Callable[[ModelType], AsyncContextManager[ModelType]]


@pytest.fixture(scope="session")
def instance_manager(
    sessionmaker: Sessionmaker,
) -> InstanceContextManager[ModelType]:
    @contextlib.asynccontextmanager
    async def wrapper(instance: ModelType) -> AsyncGenerator[ModelType, None]:
        async with sessionmaker() as session:
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
        try:
            yield instance
        finally:
            async with sessionmaker() as session:
                cursor = await session.execute(
                    sa.select(
                        sa.exists(type(instance)).where(
                            type(instance).id == instance.id
                        )
                    )
                )
                if cursor.scalar():
                    await session.delete(instance)
                    await session.commit()

    return wrapper
