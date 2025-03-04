# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
from dependency_injector import containers, providers

from src.core.infrastructure.di.core_container import CoreContainer
from src.server.application.use_cases.user_use_case import UserUseCase
from src.server.domain.services.user_service import UserService
from src.server.infrastructure.repositories.user_repository import UserRepository


class UserContainer(containers.DeclarativeContainer):
    core_container = providers.Container(CoreContainer)

    user_repository = providers.Singleton(
        UserRepository,
        database=core_container.provided.database,
    )

    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
    )

    user_use_case = providers.Factory(
        UserUseCase,
        user_service=user_service,
    )
