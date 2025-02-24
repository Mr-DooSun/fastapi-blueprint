# -*- coding: utf-8 -*-
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class ResponseFormatterMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # JSONResponse만 처리
        if isinstance(response, JSONResponse):
            original_data = await response.json()

            # DTO 타입에 맞춰 응답 포맷팅
            formatted_response = {
                "success": True,
                "message": "Request processed successfully",
                "data": original_data,
            }

            # 포맷팅 된 응답을 JSONResponse로 반환
            return JSONResponse(
                content=formatted_response,
                status_code=response.status_code,
                media_type="application/json",
            )

        # JSONResponse가 아니면 그대로 반환
        return response
