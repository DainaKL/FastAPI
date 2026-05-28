from datetime import datetime
from typing import List, Optional
from pydantic import field_validator, ConfigDict

from src.schemas.base import BaseSchema
from src.schemas.category import Category
from src.schemas.location import Location
from src.schemas.users import User
from src.schemas.post_image import PostImage


class PostBase(BaseSchema):
    title: str
    text: str
    pub_date: Optional[datetime] = None
    is_published: bool = True

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


class PostCreate(BaseSchema):
    title: str
    text: str
    pub_date: Optional[datetime] = None
    is_published: bool = True
    location_id: int | None = None
    category_id: int | None = None


class PostUpdate(BaseSchema):
    title: str | None = None
    text: str | None = None
    pub_date: datetime | None = None
    is_published: bool | None = None
    location_id: int | None = None
    category_id: int | None = None


class Post(PostBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    author: User
    location: Optional[Location] = None
    category: Optional[Category] = None
    created_at: datetime
    images: List[PostImage] = []
