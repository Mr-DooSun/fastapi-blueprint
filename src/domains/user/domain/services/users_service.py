# -*- coding: utf-8 -*-

from src.domains.core.domain.entities.user.users_entity import (
    CoreCreateUsersEntity,
    CoreUpdateUsersEntity,
    CoreUsersEntity,
)
from src.domains.core.domain.services.base_service import BaseService
from src.domains.user.infrastructure.repositories.users_repository import (
    UsersRepository,
)


class UsersService(
    BaseService[CoreCreateUsersEntity, CoreUsersEntity, CoreUpdateUsersEntity]
):
    def __init__(self, users_repository: UsersRepository) -> None:
        super().__init__(
            base_repository=users_repository,
            create_entity=CoreCreateUsersEntity,
            return_entity=CoreUsersEntity,
            update_entity=CoreUpdateUsersEntity,
        )
