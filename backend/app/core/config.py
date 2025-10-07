from functools import lru_cache
from pydantic import BaseSettings, AnyHttpUrl
from typing import Optional


class Settings(BaseSettings):
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    database_url: str
    jwt_secret: str
    jwt_access_expires_min: int = 15
    jwt_refresh_expires_days: int = 7
    password_hash_salt_rounds: int = 3
    osrm_base_url: Optional[AnyHttpUrl] = None
    log_level: str = "info"
    rate_limit_per_minute: int = 5
    cors_origins: list[AnyHttpUrl] = ["http://localhost:3000", "http://localhost:8080"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
