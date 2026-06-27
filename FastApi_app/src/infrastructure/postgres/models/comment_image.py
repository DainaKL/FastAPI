from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.infrastructure.postgres.database import Base


class CommentImage(Base):
    __tablename__ = "comment_image"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    comment_id = Column(
        Integer, ForeignKey("blog_comment.id", ondelete="CASCADE"), nullable=False
    )

    comment = relationship("Comment", back_populates="images")
