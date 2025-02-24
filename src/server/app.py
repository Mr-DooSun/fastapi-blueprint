# -*- coding: utf-8 -*-
from fastapi import FastAPI

from src.core.middleware.exception_middleware import ExceptionMiddleware
from src.core.middleware.response_middleware import ResponseFormatterMiddleware
from src.server.application.controllers import health_check_controller, user_controller
from src.server.infrastructure.di.container import ServerContainer

container = None


def create_container():
    container = ServerContainer()
    container.wire(packages=["src.server.application.controllers"])

    container.config.from_yaml("./config.yml")

    return container


def create_app():
    global container
    container = create_container()

    app = FastAPI(docs_url="/docs")
    app.add_middleware(ExceptionMiddleware)
    app.add_middleware(ResponseFormatterMiddleware)

    app.include_router(router=health_check_controller.router)
    app.include_router(router=user_controller.router)

    return app


app = create_app()
