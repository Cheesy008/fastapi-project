import os
from functools import lru_cache
from pathlib import Path
from typing import Sequence, Optional

from pydantic import BaseSettings, PostgresDsn, validator

BASE_DIR = Path(__file__).resolve().parent.parent


class EnvBaseSettings(BaseSettings):
    class Config:
        env_file = ".env"


class AppSettings(EnvBaseSettings):
    name: str = "ffbc"
    debug: bool = False
    secret_key: str = "secret"
    cors_origins: Sequence[str] | str = "*"

    algorithm: str = "HS256"
    access_token_expires_minutes: int = 15
    refresh_token_expires_minutes: int = 20

    class Config:
        env_prefix = "app_"


class PostgresSettings(EnvBaseSettings):
    scheme: str = "postgresql+asyncpg"
    host: str
    user: str
    password: str
    db: str
    sqlalchemy_database_uri: Optional[PostgresDsn] = None

    class Config:
        env_prefix = "postgres_"

    @validator("sqlalchemy_database_uri", pre=True)
    def assemble_db_connection(cls, v, values):
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme=values.get("scheme"),
            user=values.get("user"),
            password=values.get("password"),
            host=values.get("host"),
            path=f"/{values.get('db') or ''}",
        )


class RedisSettings(EnvBaseSettings):
    host: str
    port: str

    class Config:
        env_prefix = "redis_"


class Settings(EnvBaseSettings):
    app: AppSettings = AppSettings()
    database: PostgresSettings = PostgresSettings()
    redis: RedisSettings = RedisSettings()
    base_dir: Path = BASE_DIR
    media_root: str = os.path.join(BASE_DIR, "mediafiles")


@lru_cache()
def get_settings() -> Settings:
    return Settings()
