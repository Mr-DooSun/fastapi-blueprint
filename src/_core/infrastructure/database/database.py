from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from urllib.parse import quote_plus

from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from src._core.infrastructure.database.config import DatabaseConfig
from src._core.infrastructure.database.exceptions import DatabaseException


def create_async_dsn(
    database_user: str,
    database_password: str,
    database_host: str,
    database_port: int,
    database_name: str,
):
    return f"postgresql+asyncpg://{database_user}:{database_password}@{database_host}:{database_port}/{database_name}"


def create_sync_dsn(
    database_user: str,
    database_password: str,
    database_host: str,
    database_port: int,
    database_name: str,
):
    return f"postgresql+psycopg://{database_user}:{database_password}@{database_host}:{database_port}/{database_name}"


class Base(DeclarativeBase):
    pass


class Database:
    def __init__(
        self,
        database_user: str,
        database_password: str,
        database_host: str,
        database_port: int,
        database_name: str,
        config: DatabaseConfig,
    ) -> None:
        dsn = create_sync_dsn(
            database_user=quote_plus(database_user),
            database_password=quote_plus(database_password),
            database_host=database_host,
            database_port=database_port,
            database_name=database_name,
        )

        async_dsn = create_async_dsn(
            database_user=quote_plus(database_user),
            database_password=quote_plus(database_password),
            database_host=database_host,
            database_port=database_port,
            database_name=database_name,
        )

        # Exclude connect_args when creating the sync engine (asyncpg-specific options)
        sync_config = config.model_dump(exclude={"connect_args"})
        self.engine = create_engine(url=dsn, **sync_config)

        self.async_engine = create_async_engine(
            url=async_dsn,
            **config.model_dump(),
        )

        self.async_session_factory = sessionmaker(
            bind=self.async_engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
        )

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        session = None

        try:
            session = self.async_session_factory()
            yield session
        except IntegrityError:
            if session:
                await session.rollback()
            raise DatabaseException(
                status_code=400,
                message="Data integrity error",
                error_code="DB_INTEGRITY_ERROR",
            )
        except Exception as e:
            if session:
                await session.rollback()
            raise DatabaseException(
                status_code=500,
                message="Internal database error",
                error_code="DB_INTERNAL_ERROR",
                details={"original_error": str(e)},
            )
        finally:
            if session:
                await session.close()

    async def dispose(self) -> None:
        await self.async_engine.dispose()
        self.engine.dispose()

    async def check_connection(self) -> bool:
        try:
            async with self.async_engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
                return True
        except Exception as e:
            raise DatabaseException(
                status_code=503,
                message="Database health check failed",
                error_code="DATABASE_UNHEALTHY",
                details={"original_error": str(e)},
            )
