"""配置：全部从环境变量来，代码里不写字面量。

约定前缀 FDE_，本地开发读 .env（不提交），部署时由编排层注入。
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="FDE_",
        extra="ignore",
    )

    app_name: str = "fde-journey"
    env: str = "dev"
    log_level: str = "INFO"

    # W2 起使用；先留槽位，验证「配置从环境来」这条链路通不通
    llm_base_url: str = "https://api.siliconflow.cn/v1"
    llm_api_key: str | None = None
    llm_model: str = "Qwen/Qwen2.5-7B-Instruct"


settings = Settings()
