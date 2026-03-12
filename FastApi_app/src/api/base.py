from fastapi import APIRouter, status, HTTPException
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from typing import List
from src.schemas.posts import Post

Base = declarative_base()

class CategoryModel(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256))
    description = Column(Text)
    slug = Column(String, unique=True, index=True)
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class LocationModel(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256))
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class PostModel(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256))
    text = Column(Text)
    pub_date = Column(DateTime)
    is_published = Column(Boolean, default=True)
    image = Column(String, nullable=True) 
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    author_id = Column(Integer) 
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

class CommentModel(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_published = Column(Boolean, default=True)
    
    post_id = Column(Integer, ForeignKey("posts.id"))
    author_id = Column(Integer)

router = APIRouter()
# Будущая база данных
fake_db = []

# GET получение списка всех постов
@router.get("/posts", response_model=List[Post])
async def get_posts():

    return fake_db # Пока что - обманка

# GET получение конкретного поста по ID
@router.get("/posts/{id}", response_model=Post)
async def get_post(id: int):
    for post in fake_db:
        if post.id == id:  # Поиск по айди поста
            return post
    raise HTTPException(status_code=404, detail="Post not found")

# POST создание нового поста
@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=Post)
async def create_post(post: Post):
    post.id = len(fake_db) + 1  # Контроль количества постов
    fake_db.append(post)
    return post

# PUT обновление существующего поста по ID
@router.put("/posts/{id}", response_model=Post)
async def update_post(id: int, updated_post: Post):
    for i, post in enumerate(fake_db):
        if post.id == id:
            updated_post.id = id
            fake_db[i] = updated_post
            return updated_post
    raise HTTPException(status_code=404, detail="Post not found")

# DELETE удаление поста по ID
@router.delete("/posts/{id}")
async def delete_post(id: int):
    for i, post in enumerate(fake_db):
        if post.id == id:
            fake_db.pop(i)
            return {"message": "Post deleted"}
    raise HTTPException(status_code=404, detail="Post not found")