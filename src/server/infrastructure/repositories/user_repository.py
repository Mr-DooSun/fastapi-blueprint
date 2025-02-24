# -*- coding: utf-8 -*-
from contextlib import AbstractAsyncContextManager
from typing import Callable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import exists

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
        return UserModel  # 유저 엔티티를 반환

    @property
    def create_entity(self):
        # 여기에서 필요한 로직으로 엔티티를 생성할 수 있음
        return CreateUserEntity

    @property
    def return_entity(self):
        # 반환할 때 사용하는 DTO 또는 엔티티 정의
        return UserEntity

    @property
    def update_entity(self):
        # 업데이트 시 사용하는 엔티티나 로직
        return UpdateUserEntity
