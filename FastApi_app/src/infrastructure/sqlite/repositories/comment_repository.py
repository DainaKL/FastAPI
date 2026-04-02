from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.infrastructure.sqlite.models import Comment
from src.infrastructure.sqlite.repositories.base import BaseRepository


class CommentRepository(BaseRepository[Comment]):
    def __init__(self, session: Session):
        super().__init__(session, Comment)

    def get_by_post(
        self, post_id: int, skip: int = 0, limit: int = 100
    ) -> List[Comment]:
        if not post_id:
            return []
        stmt = (
            select(Comment).where(Comment.post_id == post_id).offset(skip).limit(limit)
        )
        return self.session.execute(stmt).scalars().all()

    def get_by_author(
        self, author_id: int, skip: int = 0, limit: int = 100
    ) -> List[Comment]:
        if not author_id:
            return []
        stmt = (
            select(Comment)
            .where(Comment.author_id == author_id)
            .offset(skip)
            .limit(limit)
        )
        return self.session.execute(stmt).scalars().all()

    def get_published(self, skip: int = 0, limit: int = 100) -> List[Comment]:
        stmt = select(Comment).offset(skip).limit(limit)
        return self.session.execute(stmt).scalars().all()
