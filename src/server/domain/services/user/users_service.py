# -*- coding: utf-8 -*-


from src.core.domain.entities.user.users_entity import (
    CoreCreateUsersEntity,
    CoreUpdateUsersEntity,
    CoreUsersEntity,
)
from src.core.domain.services.base_service import BaseService
from src.server.infrastructure.repositories.user.users_repository import UsersRepository


class UsersService(BaseService):
    def __init__(self, users_repository: UsersRepository) -> None:
        super().__init__(base_repository=users_repository)

    @property
    def create_entity(self):
        return CoreCreateUsersEntity

    @property
    def return_entity(self):
        return CoreUsersEntity

    @property
    def update_entity(self):
        return CoreUpdateUsersEntity
