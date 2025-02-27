# -*- coding: utf-8 -*-


from src.core.applications.dtos.user_dto import CreateUserDto, UpdateUserDto
from src.core.applications.responses.user_response import UserResponse
from src.core.applications.use_cases.base_use_case import BaseUseCase
from src.server.domain.services.user_service import UserService


class UserUseCase(BaseUseCase):
    def __init__(self, user_service: UserService) -> None:
        super().__init__(base_service=user_service)

    @property
    def create_dto(self):
        return CreateUserDto

    @property
    def response_template(self):
        return UserResponse

    @property
    def update_dto(self):
        return UpdateUserDto
