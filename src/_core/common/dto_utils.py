from typing import TypeVar

from src._core.application.dtos.base_request import BaseRequest
from src._core.application.dtos.base_response import BaseResponse
from src._core.domain.entities.entity import Entity

EntityType = TypeVar("EntityType", bound=Entity)
RequestDtoType = TypeVar("RequestDtoType", bound=BaseRequest)
ResponseDtoType = TypeVar("ResponseDtoType", bound=BaseResponse)


def dtos_to_entities(
    dtos: list[RequestDtoType], entity_cls: type[EntityType]
) -> list[EntityType]:
    return [dto.to_entity(entity_cls) for dto in dtos]


def entities_to_dtos(
    entities: list[EntityType], dto_cls: type[ResponseDtoType]
) -> list[ResponseDtoType]:
    return [dto_cls.from_entity(entity) for entity in entities]
