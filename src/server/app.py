# -*- coding: utf-8 -*-
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.middleware.exception_middleware import ExceptionMiddleware
from src.server.infrastructure.bootstrap.admin_registry import setup_admin_views
from src.server.infrastructure.bootstrap.route_registry import register_routes
from src.server.infrastructure.di.server_container import ServerContainer

container = None


def create_container():
    container = ServerContainer()
    container.wire(packages=["src.server.application.controllers"])

    return container


def create_app():
    global container
    container = create_container()

    app = FastAPI(docs_url="/docs")
    app.add_middleware(ExceptionMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    register_routes(app=app)
    setup_admin_views(app=app, database=container.core_container.database())

    return app


app = create_app()
