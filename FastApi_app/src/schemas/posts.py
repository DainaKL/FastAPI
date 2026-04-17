from datetime import datetime
from pydantic import field_validator

from src.schemas.base import BaseSchema


class PostBase(BaseSchema):
    title: str
    text: str
    pub_date: datetime
    is_published: bool = True
    image: str | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        if len(v) < 3:
            raise ValueError("Заголовок должен содержать минимум 3 символа")
        if len(v) > 256:
            raise ValueError("Заголовок должен содержать максимум 256 символов")
        return v

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str) -> str:
        if len(v) < 1:
            raise ValueError("Текст поста не может быть пустым")
        if len(v) > 10000:
            raise ValueError("Текст поста должен содержать максимум 10000 символов")
        return v


class PostCreate(PostBase):
    author_id: int
    location_id: int | None = None
    category_id: int | None = None


class PostUpdate(BaseSchema):
    title: str | None = None
    text: str | None = None
    pub_date: datetime | None = None
    is_published: bool | None = None
    location_id: int | None = None
    category_id: int | None = None
    image: str | None = None


class Post(PostBase):
    id: int
    author_id: int
    location_id: int | None = None
    category_id: int | None = None
    created_at: datetime
