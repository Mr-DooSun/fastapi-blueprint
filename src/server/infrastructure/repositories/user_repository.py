# -*- coding: utf-8 -*-
from contextlib import AbstractAsyncContextManager
from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.domain.entities.user_entity import (
    CreateUserEntity,
    UpdateUserEntity,
    UserEntity,
)
from src.core.infrastructure.database.models.user_model import UserModel
from src.core.infrastructure.repositories.base_repository import BaseRepository

SessionFactory = Callable[..., AbstractAsyncContextManager[AsyncSession]]


class UserRepository(BaseRepository):
    def __init__(self, session: SessionFactory) -> None:
        super().__init__(session=session)

    @property
    def model(self):
        return UserModel

    @property
    def create_entity(self):
        return CreateUserEntity

    @property
    def return_entity(self):
        return UserEntity

    @property
    def update_entity(self):
        return UpdateUserEntity
