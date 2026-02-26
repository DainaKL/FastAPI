from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Модели из Джанго на ФастАПИ с помощью базовых моделей

# Пользователь
class User(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    first_name: str = ""
    last_name: str = ""

# Категория
class Category(BaseModel):
    id: Optional[int] = None
    title: str
    description: str
    slug: str
    is_published: bool = True
    created_at: datetime = Field(default_factory=datetime.now)

# Местоположение
class Location(BaseModel):
    id: Optional[int] = None
    name: str
    is_published: bool = True
    created_at: datetime = Field(default_factory=datetime.now)

# Пост
class Post(BaseModel):
    id: Optional[int] = None
    title: str
    text: str
    pub_date: datetime = Field(default_factory=datetime.now)
    image: Optional[str] = None
    author_id: int
    location_id: Optional[int] = None
    category_id: Optional[int] = None
    is_published: bool = True
    created_at: datetime = Field(default_factory=datetime.now)

# Комментарий
class Comment(BaseModel):
    id: Optional[int] = None
    text: str
    post_id: int
    author_id: int
    created_at: datetime = Field(default_factory=datetime.now)