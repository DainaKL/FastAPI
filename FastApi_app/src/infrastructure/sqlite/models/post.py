from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.infrastructure.sqlite.database import Base


class Post(Base):
    __tablename__ = "blog_post"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256))
    text = Column(Text)
    pub_date = Column(DateTime(timezone=True))
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    author_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    location_id = Column(
        Integer, ForeignKey("blog_location.id", ondelete="SET NULL"), nullable=True
    )
    category_id = Column(
        Integer, ForeignKey("blog_category.id", ondelete="SET NULL"), nullable=True
    )

    author = relationship("User", back_populates="posts")
    location = relationship("Location", back_populates="posts")
    category = relationship("Category", back_populates="posts")
    images = relationship(
        "PostImage", back_populates="post", cascade="all, delete-orphan"
    )
    comments = relationship(
        "Comment", back_populates="post", cascade="all, delete-orphan"
    )
