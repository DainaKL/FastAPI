from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from src.infrastructure.sqlite.database import Base


class Post(Base):
    __tablename__ = "blog_post"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(256))
    text: Mapped[str] = mapped_column(Text)
    pub_date: Mapped[datetime] = mapped_column(DateTime)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True)
    image: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    author_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("auth_user.id", ondelete="CASCADE")
    )
    location_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("blog_location.id", ondelete="SET NULL"), nullable=True
    )
    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("blog_category.id", ondelete="SET NULL"), nullable=True
    )
