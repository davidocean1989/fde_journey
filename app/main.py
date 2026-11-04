"""FastAPI 入口：只做三件事——创建 app、挂路由、注册异常处理器。

铁律：业务逻辑一行都不许写在这个文件里。
任何人打开 main.py 应该能一屏看懂整个服务的形状。
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI

from app.api import health
from app.config import settings
from app.core.errors import AppError, app_error_handler, unhandled_error_handler

structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(ensure_ascii=False),
    ],
)
log = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # 启动时只做一次重活（建连接、加载索引），别在请求里反复做
    log.info("app_start", app=settings.app_name, env=settings.env)
    app.state.ready = True
    yield
    app.state.ready = False
    log.info("app_stop", app=settings.app_name)


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)
    app.include_router(health.router)
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(Exception, unhandled_error_handler)
    return app


app = create_app()
