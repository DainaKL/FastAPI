from pydantic_settings import BaseSettings
from pydantic import SecretStr
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "FastAPI App"
    DEBUG: bool = True

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SECRET_AUTH_KEY: SecretStr
    AUTH_ALGORITHM: str = "HS256"

    POSTGRES_HOST: str = "localhost"
    POSTGRES_DB: str = "fastapi_db"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_SCHEMA: str = "application"

    PORT: int = 8000
    ROOT_PATH: str = ""
    ORIGINS: List[str] = []

    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def DATABASE_SYNC_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()