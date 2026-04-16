from typing import List

from fastapi import HTTPException

from src.core.exceptions.database_exceptions import (
    CommentNotFoundException, DatabaseOperationException)
from src.core.exceptions.domain_exceptions import \
    CommentNotFoundException as DomainCommentNotFoundException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.comment_repository import \
    CommentRepository
from src.schemas.comments import Comment, CommentCreate, CommentUpdate


class CommentUseCases:
    def __init__(self):
        self._database = database

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Comment]:
        with self._database.session() as session:
            repo = CommentRepository(session)
            try:
                comments = repo.get_all(skip=skip, limit=limit)
                return [
                    Comment.model_validate(c, from_attributes=True) for c in comments
                ]
            except DatabaseOperationException as e:
                raise HTTPException(status_code=500, detail=e.get_detail())

    async def get_published(self, skip: int = 0, limit: int = 100) -> List[Comment]:
        with self._database.session() as session:
            repo = CommentRepository(session)
            try:
                comments = repo.get_published(skip=skip, limit=limit)
                return [
                    Comment.model_validate(c, from_attributes=True) for c in comments
                ]
            except DatabaseOperationException as e:
                raise HTTPException(status_code=500, detail=e.get_detail())

    async def get_by_id(self, comment_id: int) -> Comment:
        with self._database.session() as session:
            repo = CommentRepository(session)
            try:
                comment = repo.get_by_id(comment_id)
                return Comment.model_validate(comment, from_attributes=True)
            except CommentNotFoundException:
                raise DomainCommentNotFoundException(comment_id=comment_id)
            except DatabaseOperationException as e:
                raise HTTPException(status_code=500, detail=e.get_detail())

    async def get_by_post(
        self, post_id: int, skip: int = 0, limit: int = 100
    ) -> List[Comment]:
        with self._database.session() as session:
            repo = CommentRepository(session)
            try:
                comments = repo.get_by_post(post_id, skip=skip, limit=limit)
                return [
                    Comment.model_validate(c, from_attributes=True) for c in comments
                ]
            except DatabaseOperationException as e:
                raise HTTPException(status_code=500, detail=e.get_detail())

    async def get_by_author(
        self, author_id: int, skip: int = 0, limit: int = 100
    ) -> List[Comment]:
        with self._database.session() as session:
            repo = CommentRepository(session)
            try:
                comments = repo.get_by_author(author_id, skip=skip, limit=limit)
                return [
                    Comment.model_validate(c, from_attributes=True) for c in comments
                ]
            except DatabaseOperationException as e:
                raise HTTPException(status_code=500, detail=e.get_detail())

    async def create(self, data: CommentCreate) -> Comment:
        with self._database.session() as session:
            repo = CommentRepository(session)
            try:
                comment_dict = data.model_dump()
                comment = repo.create(**comment_dict)
                return Comment.model_validate(comment, from_attributes=True)
            except DatabaseOperationException as e:
                raise HTTPException(status_code=500, detail=e.get_detail())

    async def update(self, comment_id: int, data: CommentUpdate) -> Comment:
        with self._database.session() as session:
            repo = CommentRepository(session)
            try:
                update_dict = {
                    k: v for k, v in data.model_dump().items() if v is not None
                }
                comment = repo.update(comment_id, **update_dict)
                return Comment.model_validate(comment, from_attributes=True)
            except CommentNotFoundException:
                raise DomainCommentNotFoundException(comment_id=comment_id)
            except DatabaseOperationException as e:
                raise HTTPException(status_code=500, detail=e.get_detail())

    async def delete(self, comment_id: int) -> None:
        with self._database.session() as session:
            repo = CommentRepository(session)
            try:
                repo.delete(comment_id)
            except CommentNotFoundException:
                raise DomainCommentNotFoundException(comment_id=comment_id)
            except DatabaseOperationException as e:
                raise HTTPException(status_code=500, detail=e.get_detail())
