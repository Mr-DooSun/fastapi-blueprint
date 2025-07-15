# -*- coding: utf-8 -*-


from src.core.application.use_cases.base_use_case import BaseUseCase
from src.core.domain.entities.user.users_entity import (
    CoreCreateUsersEntity,
    CoreUpdateUsersEntity,
    CoreUsersEntity,
)
from src.server.domain.services.user.users_service import UsersService


class UsersUseCase(BaseUseCase):
    def __init__(self, users_service: UsersService) -> None:
        super().__init__(base_service=users_service)

    @property
    def create_entity(self):
        return CoreCreateUsersEntity

    @property
    def return_entity(self):
        return CoreUsersEntity

    @property
    def update_entity(self):
        return CoreUpdateUsersEntity
