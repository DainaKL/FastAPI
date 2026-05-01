from typing import Type
from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.infrastructure.sqlite.models.comment import Comment as CommentModel
from src.schemas.comments import CommentCreate as CommentSchema
from src.core.exceptions.database_exceptions import DatabaseOperationException


class CommentRepository:
    def __init__(self):
        self._model: Type[CommentModel] = CommentModel

    def get_by_id(self, session: Session, comment_id: int):
        if comment_id <= 0:
            return None
        query = select(self._model).where(self._model.id == comment_id)
        return session.scalar(query)

    def get_all(self, session: Session, skip: int = 0, limit: int = 100):
        query = select(self._model).offset(skip).limit(limit)
        return list(session.scalars(query).all())

    def get_published(self, session: Session, skip: int = 0, limit: int = 100):
        query = (
            select(self._model)
            .where(self._model.is_published == True)
            .offset(skip)
            .limit(limit)
        )
        return list(session.scalars(query).all())

    def get_by_post(
        self, session: Session, post_id: int, skip: int = 0, limit: int = 100
    ):
        query = (
            select(self._model)
            .where(self._model.post_id == post_id)
            .offset(skip)
            .limit(limit)
        )
        return list(session.scalars(query).all())

    def get_by_author(
        self, session: Session, author_id: int, skip: int = 0, limit: int = 100
    ):
        query = (
            select(self._model)
            .where(self._model.author_id == author_id)
            .offset(skip)
            .limit(limit)
        )
        return list(session.scalars(query).all())

    def create(self, session: Session, comment: CommentSchema) -> CommentModel:
        try:
            query = (
                insert(self._model).values(comment.model_dump()).returning(self._model)
            )
            return session.scalar(query)
        except IntegrityError as e:
            raise DatabaseOperationException("create", str(e))

    def update(self, session: Session, comment_id: int, **kwargs):
        query = (
            update(self._model)
            .where(self._model.id == comment_id)
            .values(**kwargs)
            .returning(self._model)
        )
        return session.scalar(query)

    def delete(self, session: Session, comment_id: int):
        query = delete(self._model).where(self._model.id == comment_id)
        result = session.execute(query)
        return result.rowcount > 0
