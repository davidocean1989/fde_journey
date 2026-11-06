# fde-journey

> FDE 学习之旅 —— 12 周全程记录，从脚本级开发到工程级交付。

FDE（Forward Deployed Engineer）12 周转型的全程工作台。
目标不是「学会写代码」，是把已有的方案判断力装上一双能干活的手。

这个仓库从第一天就按「公开可看」的标准写：所有代码、测试、文档都是 12 周的原始记录，
包括做错和返工的部分。面试时它比简历上的形容词有用。

## 进度

| 周 | 主题 | 状态 |
|---|---|---|
| W1 | 认知对齐 + 环境接管（工程底座） | 进行中 |
| W2–W12 | LLM API → Agent → RAG → 评测 → MCP → 工程化 → 旗舰项目 → 求职 | 未开始 |

## 当前状态

| 项 | 状态 |
|---|---|
| W1 交付：仓库骨架 + 覆盖率 ≥50% | ✅ 骨架跑通，覆盖率 91% |
| 工具链四件套 | ✅ uv / ruff / pytest / pydantic |
| 健康检查分层 | ✅ `/healthz` + `/readyz` |
| 统一错误形状 | ✅ `{"error": {code, message, request_id}}`（404 尚未纳入，见下） |

## 怎么跑

```bash
uv sync                                  # 装依赖（自动用 3.12）
uv run uvicorn app.main:app --reload     # 起服务
uv run pytest                            # 测试 + 覆盖率（低于 50% 直接红）
uv run ruff check .                      # 静态检查
```

## 目录约定

```
app/
├── main.py       # 只做装配：创建 app、挂路由、注册异常处理器
├── config.py     # 配置全部从环境变量来（前缀 FDE_）
├── api/          # HTTP 边界：health.py，W4 起加 search.py / chat.py
├── core/         # 横切能力：errors.py，W2 起加 llm.py
├── retrieval/    # W4 起：ingest / chunker / store / hybrid
└── eval/         # W5 起：评测
tests/
```

## 已知待办（W1 的练习题）

1. `GET /nope` 目前返回 FastAPI 默认的 `{"detail":"Not Found"}`，没走统一错误形状 ——
   因为 Starlette 的 `HTTPException` 不经过通用 `Exception` handler。
   练习：注册 `HTTPException` 的 handler，把 404/422 也变成统一形状，并补一条测试。
2. `/readyz` 目前只有 `config` 一项。W2 接上 LLM 后，把「API key 是否存在、上游是否可达」加进去。
3. `.ruff_cache/`、`.venv/`、`.env` 已在 `.gitignore`；`uv.lock` 必须提交。
