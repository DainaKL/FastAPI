from typing import List

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from src.core.exceptions.database_exceptions import (
    CommentNotFoundException, DatabaseOperationException)
from src.infrastructure.sqlite.models.comment import Comment as CommentModel


class CommentRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self, skip: int = 0, limit: int = 100) -> List[CommentModel]:
        try:
            stmt = select(CommentModel).offset(skip).limit(limit)
            return list(self.session.execute(stmt).scalars().all())
        except SQLAlchemyError as e:
            raise DatabaseOperationException("get_all", str(e))

    def get_published(self, skip: int = 0, limit: int = 100) -> List[CommentModel]:
        try:
            stmt = (
                select(CommentModel)
                .where(CommentModel.is_published == True)
                .offset(skip)
                .limit(limit)
            )
            return list(self.session.execute(stmt).scalars().all())
        except SQLAlchemyError as e:
            raise DatabaseOperationException("get_published", str(e))

    def get_by_id(self, comment_id: int) -> CommentModel:
        try:
            stmt = select(CommentModel).where(CommentModel.id == comment_id)
            comment = self.session.execute(stmt).scalar_one_or_none()
            if not comment:
                raise CommentNotFoundException(comment_id=comment_id)
            return comment
        except CommentNotFoundException:
            raise
        except SQLAlchemyError as e:
            raise DatabaseOperationException("get_by_id", str(e))

    def get_by_post(
        self, post_id: int, skip: int = 0, limit: int = 100
    ) -> List[CommentModel]:
        try:
            stmt = (
                select(CommentModel)
                .where(CommentModel.post_id == post_id)
                .offset(skip)
                .limit(limit)
            )
            return list(self.session.execute(stmt).scalars().all())
        except SQLAlchemyError as e:
            raise DatabaseOperationException("get_by_post", str(e))

    def get_by_author(
        self, author_id: int, skip: int = 0, limit: int = 100
    ) -> List[CommentModel]:
        try:
            stmt = (
                select(CommentModel)
                .where(CommentModel.author_id == author_id)
                .offset(skip)
                .limit(limit)
            )
            return list(self.session.execute(stmt).scalars().all())
        except SQLAlchemyError as e:
            raise DatabaseOperationException("get_by_author", str(e))

    def create(self, **kwargs) -> CommentModel:
        try:
            comment = CommentModel(**kwargs)
            self.session.add(comment)
            self.session.flush()
            self.session.refresh(comment)
            return comment
        except IntegrityError as e:
            self.session.rollback()
            raise DatabaseOperationException("create", str(e))
        except SQLAlchemyError as e:
            self.session.rollback()
            raise DatabaseOperationException("create", str(e))

    def update(self, comment_id: int, **kwargs) -> CommentModel:
        try:
            comment = self.get_by_id(comment_id)
            for key, value in kwargs.items():
                if hasattr(comment, key):
                    setattr(comment, key, value)
            self.session.flush()
            self.session.refresh(comment)
            return comment
        except CommentNotFoundException:
            raise
        except SQLAlchemyError as e:
            self.session.rollback()
            raise DatabaseOperationException("update", str(e))

    def delete(self, comment_id: int) -> None:
        try:
            comment = self.get_by_id(comment_id)
            self.session.delete(comment)
            self.session.flush()
        except CommentNotFoundException:
            raise
        except SQLAlchemyError as e:
            self.session.rollback()
            raise DatabaseOperationException("delete", str(e))
