from datetime import datetime
from typing import List, Optional
from pydantic import field_validator, ConfigDict

from src.schemas.base import BaseSchema
from src.schemas.comment_image import CommentImage


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


class CommentCreate(BaseSchema):
    text: str
    is_published: bool = True
    post_id: int


class CommentUpdate(BaseSchema):
    text: str | None = None
    is_published: bool | None = None


class Comment(CommentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    author_id: int
    post_id: int
    created_at: datetime
    images: List[CommentImage] = []
