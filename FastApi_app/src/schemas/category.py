import re
from datetime import datetime
from pydantic import field_validator

from src.schemas.base import BaseSchema


class CategoryBase(BaseSchema):
    title: str
    description: str | None = None
    slug: str
    is_published: bool = True

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        if len(v) < 3:
            raise ValueError("Название категории должно содержать минимум 3 символа")
        if len(v) > 256:
            raise ValueError(
                "Название категории должно содержать максимум 256 символов"
            )
        return v

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, v: str) -> str:
        if not re.match(r"^[a-z0-9_-]+$", v):
            raise ValueError(
                "Slug может содержать только строчные буквы, цифры, дефисы и подчеркивания"
            )
        if len(v) < 3:
            raise ValueError("Slug должен содержать минимум 3 символа")
        if len(v) > 100:
            raise ValueError("Slug должен содержать максимум 100 символов")
        return v


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseSchema):
    title: str | None = None
    description: str | None = None
    slug: str | None = None
    is_published: bool | None = None


class Category(CategoryBase):
    id: int
    created_at: datetime
