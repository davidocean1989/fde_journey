"""统一的错误形状。

生产里最贵的成本不是 bug，是「每次报错长得都不一样」。
W1 就把形状钉死：{"error": {"code", "message", "request_id"}}，
后面所有模块抛 AppError，不各自拼 dict。
"""

from __future__ import annotations

import structlog
from fastapi import Request
from fastapi.responses import JSONResponse

log = structlog.get_logger()


class AppError(Exception):
    """业务可预期错误。code 给机器看，message 给人看。"""

    code = "internal_error"
    status_code = 500

    def __init__(self, message: str, *, code: str | None = None, status_code: int | None = None):
        super().__init__(message)
        self.message = message
        if code is not None:
            self.code = code
        if status_code is not None:
            self.status_code = status_code


class BadRequestError(AppError):
    code = "bad_request"
    status_code = 400


class UpstreamError(AppError):
    """上游（LLM / 向量库 / 第三方 API）不可用。"""

    code = "upstream_unavailable"
    status_code = 502


def _payload(request: Request, code: str, message: str) -> dict:
    return {
        "error": {
            "code": code,
            "message": message,
            "request_id": getattr(request.state, "request_id", None),
        }
    }


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    log.warning("app_error", code=exc.code, path=request.url.path, detail=exc.message)
    return JSONResponse(
        status_code=exc.status_code, content=_payload(request, exc.code, exc.message)
    )


async def unhandled_error_handler(request: Request, exc: Exception) -> JSONResponse:
    log.exception("unhandled_error", path=request.url.path)
    return JSONResponse(
        status_code=500,
        content=_payload(request, "internal_error", "服务内部错误，请带 request_id 反馈"),
    )
