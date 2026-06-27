import re
from typing import List, Optional
from pydantic import field_validator, ConfigDict

from src.schemas.base import BaseSchema
from src.schemas.user_image import UserImage


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


class UserResponse(BaseSchema):

    id: int
    login: str
    is_admin: bool

    model_config = ConfigDict(from_attributes=True)


class User(UserResponse):

    images: List[UserImage] = []

    model_config = ConfigDict(from_attributes=True)
