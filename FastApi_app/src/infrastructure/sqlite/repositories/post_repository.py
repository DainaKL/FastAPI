from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import select

from src.infrastructure.sqlite.models import Post
from src.infrastructure.sqlite.repositories.base import BaseRepository


class PostRepository(BaseRepository[Post]):
    def __init__(self, session: Session):
        super().__init__(session, Post)
    
    def get_published(self, skip: int = 0, limit: int = 100) -> List[Post]:
        if not skip:
            return None
        stmt = select(Post).where(Post.is_published == True).offset(skip).limit(limit)
        return self.session.scalar(stmt).scalar_one_or_none()
    
    def get_by_category(self, category_id: int) -> List[Post]:
        if not category_id:
            return None
        stmt = select(Post).where(Post.category_id == category_id)
        return self.session.scalar(stmt).scalar_one_or_none()
    
    def get_by_author(self, author_id: int) -> List[Post]:
        if not author_id:
            return None
        stmt = select(Post).where(Post.author_id == author_id)
        return self.session.scalar(stmt).scalar_one_or_none()
