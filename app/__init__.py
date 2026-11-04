"""FDE Journey 应用包。

分层约定（12 周内只往里填，不重排）：
    api/      HTTP 边界，只做参数解析与响应
    core/     横切能力：配置之外的基础设施（错误、日志、LLM 客户端）
    retrieval/ RAG 相关（W4 起）
    eval/     评测（W5 起）
"""
