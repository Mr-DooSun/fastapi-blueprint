# -*- coding: utf-8 -*-
from dependency_injector import containers, providers
from minio import Minio

from src.core.applications.messaging.rabbitmq_publisher import RabbitMQPublisher
from src.core.domain.services.base_service import BaseService
from src.core.infrastructure.database.database import Database
from src.core.infrastructure.messaging.rabbitmq_manager import RabbitMQManager
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

    minio_client = providers.Singleton(
        Minio,
        endpoint=config.minio.endpoint,
        access_key=config.minio.access_key,
        secret_key=config.minio.secret_key,
        secure=False,  # HTTPS가 아닌 경우 False 설정
    )

    rabbitmq_manager = providers.Singleton(
        RabbitMQManager,
        host=config.rabbitmq.host,
        port=config.rabbitmq.port,
    )

    rabbitmq_publisher = providers.Factory(
        RabbitMQPublisher, rabbitmq_manager=rabbitmq_manager
    )

    base_repository = providers.Singleton(
        BaseRepository,
        database=database,
    )

    # 만약, 상태를 공유하는 비즈니스 로직일 경우에는, Factory가 아니라 Singleton으로 생성하는게 좋다
    base_service = providers.Factory(
        BaseService,
        base_repository=base_repository,
    )
