# -*- coding: utf-8 -*-
from dependency_injector import containers, providers

from src.core.infrastructure.di.core_container import CoreContainer
from src.server.infrastructure.di.containers.user_container import UserContainer


class ServerContainer(containers.DeclarativeContainer):
    core_container: CoreContainer = providers.Container(CoreContainer)

    user_container: UserContainer = providers.Container(
        UserContainer, core_container=core_container
    )
