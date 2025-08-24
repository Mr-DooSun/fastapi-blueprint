# -*- coding: utf-8 -*-
import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.domains.core.application.routers.api import docs_router, health_check_router
from src.domains.core.middleware.exception_middleware import ExceptionMiddleware


def create_app():
    """API Gateway - 마이크로서비스들을 통합하는 진입점"""
    app = FastAPI(
        title="FastAPI Layered Architecture",
        description="DDD 기반 마이크로서비스 API Gateway",
        version="1.0.0",
        docs_url="/docs-swagger",
        redoc_url="/docs-redoc",
    )

    # 미들웨어 설정
    app.add_middleware(ExceptionMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 공통 라우터
    app.include_router(router=health_check_router.router, tags=["status"])
    app.include_router(router=docs_router.router, tags=["docs"])

    # 프록시 라우터들
    setup_proxy_routes(app)

    return app


def setup_proxy_routes(app: FastAPI):
    """마이크로서비스로 프록시하는 라우터 설정"""

    @app.api_route(
        "/api/user/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"]
    )
    async def proxy_user_service(path: str, request):
        """User 서비스로 프록시"""
        async with httpx.AsyncClient() as client:
            url = f"http://localhost:8001/user/v1/{path}"
            response = await client.request(
                method=request.method,
                url=url,
                headers=dict(request.headers),
                content=await request.body(),
            )
            return response.json()

    @app.websocket("/api/chat/{path:path}")
    async def proxy_chat_service(websocket, path: str):
        """Chat 서비스로 WebSocket 프록시"""
        # WebSocket 프록시는 복잡하므로 우선 직접 연결 안내
        await websocket.accept()
        await websocket.send_text("Chat service: ws://localhost:8002/chat/v1/ws/chat")
        await websocket.close()


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.apps.gateway.app:app", reload=True, host="127.0.0.1", port=8000)
