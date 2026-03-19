from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import select

from src.infrastructure.sqlite.models import Post
from src.infrastructure.sqlite.repositories.base import BaseRepository


class PostRepository(BaseRepository[Post]):
    def __init__(self, session: Session):
        super().__init__(session, Post)
    
    def get_published(self, skip: int = 0, limit: int = 100) -> List[Post]:
        stmt = select(Post).where(Post.is_published == True).offset(skip).limit(limit)
        return list(self.session.execute(stmt).scalars().all())
    
    def get_by_category(self, category_id: int) -> List[Post]:
        stmt = select(Post).where(Post.category_id == category_id)
        return list(self.session.execute(stmt).scalars().all())
    
    def get_by_author(self, author_id: int) -> List[Post]:
        stmt = select(Post).where(Post.author_id == author_id)
        return list(self.session.execute(stmt).scalars().all())
