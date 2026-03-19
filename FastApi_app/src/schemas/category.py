from datetime import datetime

from pydantic import Field

from src.schemas.base import BaseSchema


class Category(BaseSchema):
    title: str
    description: str
    slug: str
    is_published: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
