from datetime import datetime

from pydantic import Field

from src.schemas.base import BaseSchema


class CategoryBase(BaseSchema):
    title: str
    description: str
    slug: str
    is_published: bool = True


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseSchema):
    title: str | None = None
    description: str | None = None
    slug: str | None = None
    is_published: bool | None = None


class Category(CategoryBase):
    id: int
    created_at: datetime | None
