from dependency_injector import containers, providers

from src._core.infrastructure.database.database import Database
from src._core.infrastructure.http.http_client import HttpClient
from src._core.infrastructure.messaging.celery_factory import create_celery_app
from src._core.infrastructure.messaging.celery_manager import CeleryManager
from src._core.infrastructure.storage.object_storage import ObjectStorage
from src._core.infrastructure.storage.object_storage_client import ObjectStorageClient


class CoreContainer(containers.DeclarativeContainer):
    config = providers.Configuration(strict=True)
    config.from_yaml("./config.yml")

    #########################################################
    # Database
    #########################################################

    database = providers.Singleton(
        Database,
        env=config.env,
        database_user=config.database.user,
        database_password=config.database.password,
        database_host=config.database.host,
        database_port=config.database.port,
        database_name=config.database.name,
    )

    #########################################################
    # HTTP Client
    #########################################################

    http_client = providers.Singleton(
        HttpClient,
        env=config.env,
    )

    #########################################################
    # Storage
    #########################################################

    # MinIO용 설정 (코드는 동일, 설정만 변경)
    # minio_client = ObjectStorageClient(
    #     access_key="minioadmin",
    #     secret_access_key="minioadmin",
    #     endpoint_url="http://localhost:9000"
    # )

    # AWS S3용 설정
    s3_client = providers.Singleton(
        ObjectStorageClient,
        access_key=config.s3.access_key,
        secret_access_key=config.s3.secret_key,
        region_name=config.s3.region,
    )

    s3_storage = providers.Factory(
        ObjectStorage,
        storage_client=s3_client,
        bucket_name=config.s3.bucket_name,
    )

    #########################################################
    # Messaging
    #########################################################

    celery_app = providers.Singleton(
        create_celery_app,
        env=config.env,
        region=config.sqs.region,
        access_key=config.sqs.access_key,
        secret_key=config.sqs.secret_key,
        queue=config.sqs.queue,
    )

    celery_manager = providers.Singleton(
        CeleryManager,
        celery_app=celery_app,
    )
