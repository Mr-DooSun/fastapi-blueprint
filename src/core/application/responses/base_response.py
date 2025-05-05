# -*- coding: utf-8 -*-
from typing import Any, Optional

from src.core.application.dtos.base_config import BaseConfig


class PaginationInfo(BaseConfig):
    current_page: int
    page_size: int
    total_items: int
    total_pages: int
    has_previous: bool
    has_next: bool
    next_page: Optional[int] = None
    previous_page: Optional[int] = None


class BaseResponse(BaseConfig):
    success: bool = True
    message: str = "Request processed successfully"
    data: Optional[Any] = None
    pagination: Optional[PaginationInfo] = None
    exists: Optional[bool] = None
