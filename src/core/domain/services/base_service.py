# -*- coding: utf-8 -*-
import logging
from abc import ABC, abstractmethod
from typing import List, Type, TypeVar

from pydantic import BaseModel

from src.core.infrastructure.repositories.base_repository import BaseRepository

CreateEntity = TypeVar("CreateEntity", bound=BaseModel)
ReturnEntity = TypeVar("ReturnEntity", bound=BaseModel)
UpdateEntity = TypeVar("UpdateEntity", bound=BaseModel)


class BaseService(ABC):
    def __init__(
        self,
        base_repository: BaseRepository,
    ) -> None:
        self.base_repository = base_repository
        self.logger = logging.getLogger(__name__)

    @property
    @abstractmethod
    def create_entity(self) -> Type[CreateEntity]:
        pass

    @property
    @abstractmethod
    def return_entity(self) -> Type[ReturnEntity]:
        pass

    @property
    @abstractmethod
    def update_entity(self) -> Type[UpdateEntity]:
        pass

    async def create_data(self, create_data: CreateEntity) -> ReturnEntity:
        data = await self.base_repository.create_data(create_data=create_data)
        return self.return_entity.model_validate(vars(data))

    async def create_datas(
        self, create_datas: List[CreateEntity]
    ) -> List[ReturnEntity]:
        datas = await self.base_repository.create_datas(create_datas=create_datas)
        return [self.return_entity.model_validate(vars(data)) for data in datas]

    async def get_datas(self, page: int, page_size: int) -> List[ReturnEntity]:
        datas = await self.base_repository.get_datas(page=page, page_size=page_size)
        return [self.return_entity.model_validate(vars(data)) for data in datas]

    async def get_data_by_data_id(self, data_id: int) -> ReturnEntity:
        data = await self.base_repository.get_data_by_data_id(data_id=data_id)
        return self.return_entity.model_validate(vars(data))

    async def get_datas_by_data_ids(self, data_ids: List[int]) -> List[ReturnEntity]:
        datas = await self.base_repository.get_datas_by_data_ids(data_ids=data_ids)
        return [self.return_entity.model_validate(vars(data)) for data in datas]

    async def count_datas(self) -> int:
        return await self.base_repository.count_datas()

    async def update_data_by_data_id(
        self, data_id: int, update_data: UpdateEntity
    ) -> ReturnEntity:
        data = await self.base_repository.update_data_by_data_id(
            data_id=data_id, update_data=update_data
        )
        return self.return_entity.model_validate(vars(data))

    async def delete_data_by_data_id(self, data_id: int) -> bool:
        return await self.base_repository.delete_data_by_data_id(data_id=data_id)
