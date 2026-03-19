from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import select

from src.infrastructure.sqlite.models import Comment
from src.infrastructure.sqlite.repositories.base import BaseRepository


class CommentRepository(BaseRepository[Comment]):
    def __init__(self, session: Session):
        super().__init__(session, Comment)
    
    def get_by_post(self, post_id: int) -> List[Comment]:
        stmt = select(Comment).where(Comment.post_id == post_id)
        return list(self.session.execute(stmt).scalars().all())
    
    def get_by_author(self, author_id: int) -> List[Comment]:
        stmt = select(Comment).where(Comment.author_id == author_id)
        return list(self.session.execute(stmt).scalars().all())
