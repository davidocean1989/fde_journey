"""健康检查分两层，这是 W1 最容易做错的地方。

/healthz  liveness  —— 进程还活着吗？给容器探针用，永远不查依赖。
/readyz   readiness —— 依赖可用吗？给负载均衡用，依赖挂了返回 503。

只有一个 /health 的后果：数据库抖一下，容器被判定死亡反复重启，
把一个 30 秒的故障放大成 10 分钟。
"""

from fastapi import APIRouter, Response, status

router = APIRouter(tags=["health"])


@router.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/readyz")
async def readyz(response: Response) -> dict[str, object]:
    # W2 起往这里加真实依赖：llm_credentials / vector_store / disk
    checks = {"config": True}
    ready = all(checks.values())
    if not ready:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return {"status": "ready" if ready else "not_ready", "checks": checks}
