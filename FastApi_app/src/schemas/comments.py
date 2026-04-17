from datetime import datetime
from pydantic import field_validator

from src.schemas.base import BaseSchema


class CommentBase(BaseSchema):
    text: str
    is_published: bool = True

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str) -> str:
        if len(v) < 1:
            raise ValueError("Текст комментария не может быть пустым")
        if len(v) > 2000:
            raise ValueError(
                "Текст комментария должен содержать максимум 2000 символов"
            )
        return v


class CommentCreate(CommentBase):
    author_id: int
    post_id: int


class CommentUpdate(BaseSchema):
    text: str | None = None
    is_published: bool | None = None


class Comment(CommentBase):
    id: int
    author_id: int
    post_id: int
    created_at: datetime
