from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.sql import func

from src.infrastructure.sqlite.database import Base


class Comment(Base):
    __tablename__ = "blog_comment"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    is_published: Mapped[bool] = mapped_column(Boolean, default=True)
    
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("posts.id"))
    author_id: Mapped[int] = mapped_column(Integer)
    