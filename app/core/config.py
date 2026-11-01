from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Typed settings loaded from environment variables / .env. No secrets in code."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "local"
    log_level: str = "INFO"

    database_url: str = Field(
        default="postgresql+psycopg://postgres:postgres@localhost:5432/moin_chatbot"
    )
    db_pool_size: int = 5
    db_max_overflow: int = 10

    allowed_origins: str = "http://localhost:3000,http://localhost:5173"

    llm_provider: str = "openai"
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    embedding_model: str = ""

    rag_top_k: int = 5
    rag_min_score: float = 0.0

    email_backend: str = "smtp"
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    lead_notify_to: str = "info@moinsystemsai.com"

    @property
    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
