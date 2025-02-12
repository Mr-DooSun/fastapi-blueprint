# -*- coding: utf-8 -*-
from dependency_injector import containers, providers

from src.core.application.services.base_service import BaseService
from src.core.infrastructure.database.database import Database
from src.core.infrastructure.repositories.base_repository import BaseRepository


class CoreContainer(containers.DeclarativeContainer):
    config = providers.Configuration(strict=True)

    database = providers.Singleton(
        Database,
        database_user=config.database.user,
        database_password=config.database.password,
        database_host=config.database.host,
        database_port=config.database.port,
        database_name=config.database.name,
    )

    base_repository = providers.Singleton(
        BaseRepository,
        session=database.provided.session,
    )

    base_service = providers.Factory(
        BaseService,
        base_repository=base_repository,
    )
