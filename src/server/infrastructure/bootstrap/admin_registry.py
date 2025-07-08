# -*- coding: utf-8 -*-
from fastapi import FastAPI
from sqladmin import Admin

from src.core.infrastructure.database.database import Database
from src.server.admin.views.user_view import UserView


def setup_admin_views(app: FastAPI, database: Database):
    admin = Admin(app=app, engine=database.engine)

    admin.add_view(UserView)
