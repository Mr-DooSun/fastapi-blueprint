from typing import Generic, TypeVar

from src._core.application.dtos.base_config import ApiConfig
from src._core.domain.entities.entity import Entity


class PaginationInfo(ApiConfig):
    current_page: int
    page_size: int
    total_items: int
    total_pages: int
    has_previous: bool
    has_next: bool
    next_page: int | None = None
    previous_page: int | None = None


class ExistsData(ApiConfig):
    exists: bool


ReturnType = TypeVar("ReturnType")


class BaseResponse(ApiConfig):
    @classmethod
    def from_entity(cls: type[ReturnType], entity: Entity) -> ReturnType:
        return cls(**entity.model_dump())


class SuccessResponse(ApiConfig, Generic[ReturnType]):
    success: bool = True
    message: str = "Request processed successfully"
    data: ReturnType | None = None
    pagination: PaginationInfo | None = None


class ErrorResponse(ApiConfig):
    success: bool = False
    message: str = "Request failed"
    error_code: str | None = None
    error_details: dict | None = None
