# -*- coding: utf-8 -*-
from fastapi import FastAPI

from src.server.application.controllers import health_check_controller
from src.server.application.controllers.user import users_controller


def register_routes(app: FastAPI):
    app.include_router(router=health_check_controller.router)
    app.include_router(router=users_controller.router)
