from typing import List

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from src.core.exceptions.database_exceptions import (
    DatabaseOperationException, PostNotFoundException)
from src.infrastructure.sqlite.models.post import Post as PostModel


class PostRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self, skip: int = 0, limit: int = 100) -> List[PostModel]:
        try:
            stmt = select(PostModel).offset(skip).limit(limit)
            return list(self.session.execute(stmt).scalars().all())
        except SQLAlchemyError as e:
            raise DatabaseOperationException("get_all", str(e))

    def get_by_id(self, post_id: int) -> PostModel:
        try:
            stmt = select(PostModel).where(PostModel.id == post_id)
            post = self.session.execute(stmt).scalar_one_or_none()
            if not post:
                raise PostNotFoundException(post_id=post_id)
            return post
        except PostNotFoundException:
            raise
        except SQLAlchemyError as e:
            raise DatabaseOperationException("get_by_id", str(e))

    def create(self, **kwargs) -> PostModel:
        try:
            post = PostModel(**kwargs)
            self.session.add(post)
            self.session.flush()
            self.session.refresh(post)
            return post
        except IntegrityError as e:
            self.session.rollback()
            raise DatabaseOperationException("create", str(e))
        except SQLAlchemyError as e:
            self.session.rollback()
            raise DatabaseOperationException("create", str(e))

    def update(self, post_id: int, **kwargs) -> PostModel:
        try:
            post = self.get_by_id(post_id)
            for key, value in kwargs.items():
                if hasattr(post, key):
                    setattr(post, key, value)
            self.session.flush()
            self.session.refresh(post)
            return post
        except PostNotFoundException:
            raise
        except SQLAlchemyError as e:
            self.session.rollback()
            raise DatabaseOperationException("update", str(e))

    def delete(self, post_id: int) -> None:
        try:
            post = self.get_by_id(post_id)
            self.session.delete(post)
            self.session.flush()
        except PostNotFoundException:
            raise
        except SQLAlchemyError as e:
            self.session.rollback()
            raise DatabaseOperationException("delete", str(e))
