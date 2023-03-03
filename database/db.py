from typing import AsyncContextManager, Callable

from dependency_injector import containers, providers

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    sessionmaker as sqlalchemy_sessionmaker,
)

Sessionmaker = Callable[..., AsyncContextManager[AsyncSession]]


def create_db_url(
    user: str, password: str | None, host: str, port: str | int, db: str
) -> str:
    return "postgresql+asyncpg://{user}{password}@{host}:{port}/{db}".format(
        user=user,
        password=f":{password}" if password else "",
        host=host,
        port=port,
        db=db,
    )


class DatabaseContainer(containers.DeclarativeContainer):
    config = providers.Configuration(strict=True)
    connection_url = providers.Singleton(
        create_db_url,
        user=config.user,
        password=config.password,
        host=config.host,
        port=config.port,
        db=config.db,
    )
    engine: providers.Singleton[AsyncEngine] = providers.Singleton(
        create_async_engine,
        url=connection_url,
        future=True,
        echo=config.echo,
    )
    sessionmaker: providers.Singleton[Sessionmaker] = providers.Singleton(
        sqlalchemy_sessionmaker,
        bind=engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
        class_=AsyncSession,
    )


class Base(DeclarativeBase):
    pass
