from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "FastAPI App"
    APP_ENV: str = "development"
    DEBUG: bool = True

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SECRET_AUTH_KEY: SecretStr = SecretStr("your-secret-key-change-in-production")
    AUTH_ALGORITHM: str = "HS256"

    DATABASE_URL: str = "sqlite+aiosqlite:///./db.sqlite3"
    DB_ECHO: bool = True

    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
