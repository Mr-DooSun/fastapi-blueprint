# -*- coding: utf-8 -*-
import traceback

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from src.core.exceptions.base_exception import BaseCustomException


class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except BaseCustomException as exc:
            return JSONResponse(
                status_code=exc.status_code, content={"message": exc.message}
            )
        except Exception as exc:
            error_trace = traceback.format_exc()
            print(error_trace)
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "message": f"Internal server error: {str(exc)}",
                },
            )
