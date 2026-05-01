from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SECRET_AUTH_KEY: SecretStr = SecretStr("your-secret-key-change-in-production")
    AUTH_ALGORITHM: str = "HS256"

    DATABASE_URL: str = "sqlite:///./db.sqlite3"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
