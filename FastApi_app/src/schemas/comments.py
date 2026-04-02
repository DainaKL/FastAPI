from datetime import datetime

from src.schemas.base import BaseSchema


class CommentBase(BaseSchema):
    text: str
    is_published: bool = True


class CommentCreate(CommentBase):
    post_id: int
    author_id: int


class CommentUpdate(BaseSchema):
    text: str | None = None
    is_published: bool | None = None


class Comment(CommentBase):
    id: int
    author_id: int
    post_id: int
    created_at: datetime
