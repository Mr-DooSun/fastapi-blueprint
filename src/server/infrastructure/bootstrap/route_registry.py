# -*- coding: utf-8 -*-
from fastapi import FastAPI

from src.server.application.controllers import health_check_controller, user_controller


def register_routes(app: FastAPI):
    app.include_router(router=health_check_controller.router)
    app.include_router(router=user_controller.router)
