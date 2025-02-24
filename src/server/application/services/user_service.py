# -*- coding: utf-8 -*-
import io

from fastapi import File, UploadFile

from src.core.application.dtos.user_dto import CreateUserDto, UpdateUserDto, UserDto
from src.core.application.services.base_service import BaseService
from src.server.infrastructure.repositories.user_repository import UserRepository


class UserService(BaseService):
    def __init__(
        self,
        user_repository: UserRepository
    ) -> None:
        super().__init__(base_repository=user_repository)
        self.users_repository = user_repository

    @property
    def create_dto(self):
        """하위 클래스에서 DTO 생성 메서드 정의"""
        return CreateUserDto

    @property
    def response_dto(self):
        """하위 클래스에서 반환 DTO 메서드 정의"""
        return UserDto

    @property
    def update_dto(self):
        """하위 클래스에서 DTO 업데이트 메서드 정의"""
        return UpdateUserDto