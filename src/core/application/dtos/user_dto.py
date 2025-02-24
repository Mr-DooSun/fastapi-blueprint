# -*- coding: utf-8 -*-


from src.core.application.dtos.base import BaseRequest, BaseResponse
from src.core.domain.entities.user_entity import (
    CreateUserEntity,
    UpdateUserEntity,
    UserEntity,
)


class UserDto(BaseResponse, UserEntity):
    pass


class CreateUserDto(BaseRequest, CreateUserEntity):
    pass


class UpdateUserDto(BaseRequest, UpdateUserEntity):
    pass
