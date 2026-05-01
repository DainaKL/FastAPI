from typing import Type
from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.infrastructure.sqlite.models.post import Post as PostModel
from src.schemas.posts import PostCreate as PostSchema
from src.core.exceptions.database_exceptions import DatabaseOperationException


class PostRepository:
    def __init__(self):
        self._model: Type[PostModel] = PostModel

    def get_by_id(self, session: Session, post_id: int):
        if post_id <= 0:
            return None
        query = select(self._model).where(self._model.id == post_id)
        return session.scalar(query)

    def get_all(self, session: Session, skip: int = 0, limit: int = 100):
        query = select(self._model).offset(skip).limit(limit)
        return list(session.scalars(query).all())

    def create(self, session: Session, post: PostSchema) -> PostModel:
        try:
            query = insert(self._model).values(post.model_dump()).returning(self._model)
            return session.scalar(query)
        except IntegrityError as e:
            raise DatabaseOperationException("create", str(e))

    def update(self, session: Session, post_id: int, **kwargs):
        query = (
            update(self._model)
            .where(self._model.id == post_id)
            .values(**kwargs)
            .returning(self._model)
        )
        return session.scalar(query)

    def delete(self, session: Session, post_id: int):
        query = delete(self._model).where(self._model.id == post_id)
        result = session.execute(query)
        return result.rowcount > 0
