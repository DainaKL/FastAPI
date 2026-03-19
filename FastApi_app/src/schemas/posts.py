from datetime import datetime
from typing import Optional

from pydantic import Field

from src.schemas.base import BaseSchema


class PostBase(BaseSchema):  
    title: str
    text: str
    pub_date: datetime
    is_published: bool
    image: str | None = None


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
