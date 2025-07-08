# -*- coding: utf-8 -*-
from sqladmin import ModelView
from sqlalchemy import class_mapper

from src.core.infrastructure.database.models.user_model import UserModel


class UserView(ModelView, model=UserModel):
    column_list = [attr.key for attr in class_mapper(UserModel).column_attrs]
