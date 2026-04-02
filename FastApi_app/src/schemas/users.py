from src.schemas.base import BaseSchema


class UserBase(BaseSchema):
    login: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseSchema):
    login: str | None = None
    password: str | None = None


class User(UserBase):
    id: int
