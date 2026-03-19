from datetime import datetime
from typing import Optional

from pydantic import Field

from src.schemas.base import BaseSchema
from src.schemas.users import User
from src.schemas.location import Location
from src.schemas.category import Category


class Post(BaseSchema):
    id: int
    title: str 
    text: str
    pub_date: datetime = Field(default_factory=datetime.now)
    is_published: bool = True
    author: User
    location: Location | None = None 
    category: Optional[Category] = None
    image: Optional[str] = None
