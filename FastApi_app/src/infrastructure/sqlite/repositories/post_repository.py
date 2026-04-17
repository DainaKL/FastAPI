from typing import Type

from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.infrastructure.sqlite.models.post import Post as PostModel
from src.schemas.posts import PostCreate as PostSchema
from src.core.exceptions.database_exceptions import PostNotFoundException, DatabaseOperationException


class PostRepository:
    def __init__(self):
        self._model: Type[PostModel] = PostModel

    def get_by_id(self, session: Session, post_id: int) -> PostModel:
        if post_id <= 0:
            raise PostNotFoundException(post_id=post_id)
        query = select(self._model).where(self._model.id == post_id)
        post = session.scalar(query)
        if not post:
            raise PostNotFoundException(post_id=post_id)
        return post

    def get_all(self, session: Session, skip: int = 0, limit: int = 100):
        query = select(self._model).offset(skip).limit(limit)
        return list(session.scalars(query).all())

    def create(self, session: Session, post: PostSchema) -> PostModel:
        query = insert(self._model).values(post.model_dump()).returning(self._model)
        try:
            return session.scalar(query)
        except IntegrityError as e:
            raise DatabaseOperationException("create", str(e))

    def update(self, session: Session, post_id: int, **kwargs) -> PostModel:
        query = update(self._model).where(self._model.id == post_id).values(**kwargs).returning(self._model)
        post = session.scalar(query)
        if not post:
            raise PostNotFoundException(post_id=post_id)
        return post

    def delete(self, session: Session, post_id: int) -> None:
        query = delete(self._model).where(self._model.id == post_id)
        result = session.execute(query)
        if result.rowcount == 0:
            raise PostNotFoundException(post_id=post_id)
