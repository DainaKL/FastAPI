from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from src.infrastructure.sqlite.database import Base


class Comment(Base):
    __tablename__ = "blog_comment"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    is_published: Mapped[bool] = mapped_column(Boolean, default=True)

    # Главная проблема
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("blog_post.id"))
    author_id: Mapped[int] = mapped_column(Integer)
