from src._core.infrastructure.database.database import Database
from src._core.infrastructure.repositories.base_repository import BaseRepository
from src.user.domain.entities.users_entity import (
    CoreCreateUsersEntity,
    CoreUpdateUsersEntity,
    CoreUsersEntity,
)
from src.user.infrastructure.database.models.users_model import UsersModel


class UsersRepository(
    BaseRepository[CoreCreateUsersEntity, CoreUsersEntity, CoreUpdateUsersEntity]
):
    def __init__(self, database: Database) -> None:
        super().__init__(
            database=database,
            model=UsersModel,
            create_entity=CoreCreateUsersEntity,
            return_entity=CoreUsersEntity,
            update_entity=CoreUpdateUsersEntity,
        )
