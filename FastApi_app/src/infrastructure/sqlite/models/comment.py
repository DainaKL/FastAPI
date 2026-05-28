from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.infrastructure.sqlite.database import Base


class Comment(Base):
    __tablename__ = "blog_comment"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_published = Column(Boolean, default=True)

    post_id = Column(
        Integer, ForeignKey("blog_post.id", ondelete="CASCADE"), nullable=False
    )
    author_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")
    images = relationship(
        "CommentImage", back_populates="comment", cascade="all, delete-orphan"
    )
