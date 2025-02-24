# -*- coding: utf-8 -*-
from datetime import datetime

from src.core.domain.entities.entity import Entity


class UserEntity(Entity):
    id: int
    username: str
    full_name: str
    email: str
    password: str
    created_at: datetime
    updated_at: datetime


class CreateUserEntity(Entity):
    username: str
    password: str
    email: str
    full_name: str


class UpdateUserEntity(Entity):
    username: str
    password: str
    email: str
    full_name: str
