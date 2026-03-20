from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import select

from src.infrastructure.sqlite.models import Comment
from src.infrastructure.sqlite.repositories.base import BaseRepository


class CommentRepository(BaseRepository[Comment]):
    def __init__(self, session: Session):
        super().__init__(session, Comment)
    
    def get_by_post(self, post_id: int) -> List[Comment]:
        if not post_id:
            return None
        stmt = select(Comment).where(Comment.post_id == post_id)
        return self.session.scalar(stmt).scalar_one_or_none()
    
    def get_by_author(self, author_id: int) -> List[Comment]:
        if not author_id:
            return None
        stmt = select(Comment).where(Comment.author_id == author_id)
        return self.session.scalar(stmt).scalar_one_or_none()
    
