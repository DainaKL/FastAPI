from pydantic_settings import BaseSettings
from pydantic import SecretStr


class Settings(BaseSettings):
    APP_NAME: str = "FastAPI App"
    APP_ENV: str = "development"
    DEBUG: bool = True

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SECRET_AUTH_KEY: SecretStr
    AUTH_ALGORITHM: str = "HS256"

    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@db:5432/fastapi_db"
    DATABASE_SYNC_URL: str = "postgresql://postgres:postgres@db:5432/fastapi_db"

    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
