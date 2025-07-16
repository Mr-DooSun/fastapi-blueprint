# -*- coding: utf-8 -*-
from fastapi import FastAPI

from src.server.application.routers.api import health_check_router
from src.server.application.routers.api.user import users_router


def register_routes(app: FastAPI):
    app.include_router(router=health_check_router.router, prefix="/v1", tags=["status"])
    app.include_router(router=users_router.router, prefix="/v1", tags=["유저"])
