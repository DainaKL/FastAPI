from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

from .database import Base


class Post(Base):
    __tablename__ = "blog_post"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256), nullable=False)
    text = Column(Text, nullable=False)
    pub_date = Column(DateTime, default=func.now())
    is_published = Column(Boolean, default=True)
    image = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())

    author_id = Column(Integer, nullable=False)
    location_id = Column(Integer, ForeignKey("blog_location.id"), nullable=True)
    category_id = Column(Integer, ForeignKey("blog_category.id"), nullable=True)


class Comment(Base):
    __tablename__ = "blog_comment"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())
    post_id = Column(Integer, ForeignKey("blog_post.id"), nullable=False)
    author_id = Column(Integer, nullable=False)


class Location(Base):
    __tablename__ = "blog_location"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)


class Category(Base):
    __tablename__ = "blog_category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
