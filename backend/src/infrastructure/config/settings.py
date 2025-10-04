from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # Application
    app_env: str = "development"
    app_host: str = "0.0.0.0"  # nosec B104 - Required for Docker container networking
    app_port: int = 8000
    log_level: str = "INFO"

    # LM Studio
    lm_studio_base_url: str = "http://127.0.0.1:1234/v1"
    lm_studio_api_key: Optional[str] = None
    lm_studio_model: Optional[str] = None
    lm_studio_max_tokens: int = 2048
    lm_studio_temperature: float = 0.7
    lm_studio_top_p: float = 0.9
    request_timeout_seconds: int = 120

    # Telegram
    telegram_bot_token: Optional[str] = None
    telegram_allowed_user_ids: Optional[str] = None

    # Frontend
    vite_api_base_url: str = "http://localhost:8000"

    # CORS
    cors_origins: str = "http://localhost:3000,http://localhost:5173"

    # Database
    database_url: str = "postgresql://postgres:postgres@localhost:5432/optimizer"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    @property
    def cors_origins_list(self) -> List[str]:
        """Get CORS origins as a list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    @property
    def telegram_allowed_user_ids_list(self) -> List[int]:
        """Get allowed Telegram user IDs as a list of integers."""
        if not self.telegram_allowed_user_ids:
            return []
        return [
            int(user_id.strip())
            for user_id in self.telegram_allowed_user_ids.split(",")
            if user_id.strip()
        ]


settings = Settings()
