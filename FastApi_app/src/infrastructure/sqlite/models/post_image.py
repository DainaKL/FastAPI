from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.infrastructure.sqlite.database import Base


class PostImage(Base):
    __tablename__ = "blog_post_image"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    post_id = Column(
        Integer, ForeignKey("blog_post.id", ondelete="CASCADE"), nullable=False
    )

    post = relationship("Post", back_populates="images")
