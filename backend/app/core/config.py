"""项目配置管理"""

from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """统一配置对象"""

    # 从 .env 读取，额外位置字段忽略，避免报错
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )

    app_name: str = "Omni Claw"
    app_env: str = "dev"

    # Provider / Model
    provider: str = Field(default="aliyun", alias="DEFAULT_PROVIDER")
    model_name: str = Field(default="qwen-max", alias="DEFAULT_MODEL")
    
    # 路径配置
    workspace_dir: str = "./workspace"
    logs_dir: str = "./logs"
    tasks_dir: str = "./tasks"
    db_path: str = "workspace/omniclaw.db"

    # 密钥（敏感）
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    openai_api_base: str | None = Field(default=None, alias="OPENAI_API_BASE")
    anthropic_api_key: str | None = Field(default=None)

@lru_cache()
def get_settings() -> Settings:
    """获取全局单例配置"""
    return Settings()

def mask_secret(value: str | None) -> str:
    """把敏感信息脱敏后展示"""
    if not value:
        return "(empty)"
    if len(value) <= 8:
        return "***"
    return f"{value[:4]}***{value[-4:]}"