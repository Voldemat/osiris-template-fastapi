from dependency_injector import containers, providers

from database import DatabaseContainer


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[".routers", ".dependencies"],
    )
    config = providers.Configuration(strict=True)
    db = providers.Container(DatabaseContainer, config=config.db)
