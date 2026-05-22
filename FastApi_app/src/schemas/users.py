import re
from pydantic import field_validator, BaseModel

from src.schemas.base import BaseSchema


class UserBase(BaseSchema):
    login: str

    @field_validator("login")
    @classmethod
    def validate_login(cls, v: str) -> str:
        if len(v) < 3:
            raise ValueError("Логин должен содержать минимум 3 символа")
        if len(v) > 50:
            raise ValueError("Логин должен содержать максимум 50 символов")
        if not re.match(r"^[a-zA-Z0-9_]+$", v):
            raise ValueError(
                "Логин может содержать только буквы, цифры и символ подчеркивания"
            )
        return v


class UserCreate(BaseSchema):
    login: str
    password: str

    @field_validator("login")
    @classmethod
    def validate_login(cls, v: str) -> str:
        if len(v) < 3:
            raise ValueError("Логин должен содержать минимум 3 символа")
        if len(v) > 50:
            raise ValueError("Логин должен содержать максимум 50 символов")
        if not re.match(r"^[a-zA-Z0-9_]+$", v):
            raise ValueError(
                "Логин может содержать только буквы, цифры и символ подчеркивания"
            )
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("Пароль должен содержать минимум 6 символов")
        if len(v) > 100:
            raise ValueError("Пароль должен содержать максимум 100 символов")
        return v


class UserUpdate(BaseSchema):
    login: str | None = None
    password: str | None = None
    is_admin: bool | None = None

    @field_validator("login")
    @classmethod
    def validate_login(cls, v: str | None) -> str | None:
        if v is not None:
            if len(v) < 3:
                raise ValueError("Логин должен содержать минимум 3 символа")
            if len(v) > 50:
                raise ValueError("Логин должен содержать максимум 50 символов")
            if not re.match(r"^[a-zA-Z0-9_]+$", v):
                raise ValueError(
                    "Логин может содержать только буквы, цифры и символ подчеркивания"
                )
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str | None) -> str | None:
        if v is not None:
            if len(v) < 6:
                raise ValueError("Пароль должен содержать минимум 6 символов")
            if len(v) > 100:
                raise ValueError("Пароль должен содержать максимум 100 символов")
        return v


class User(UserBase):
    id: int
    is_admin: bool = False

    class Config:
        from_attributes = True
