from fastapi import HTTPException, status
from typing import List
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.comment_repository import CommentRepository
from src.infrastructure.sqlite.models.comment import Comment as CommentModel
from src.schemas.comments import CommentCreate, CommentUpdate, Comment


class CommentUseCases:
    def __init__(self):
        self._database = database

    async def create(self, data: CommentCreate) -> Comment:
        with self._database.session() as session:
            repo = CommentRepository(session)
            comment = CommentModel(**data.model_dump())
            created = repo.create(comment)
            return Comment.model_validate(created, from_attributes=True)

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Comment]:
        with self._database.session() as session:
            repo = CommentRepository(session)
            comments = repo.get_all(skip=skip, limit=limit)
            return [Comment.model_validate(c, from_attributes=True) for c in comments]

    async def get_published(self, skip: int = 0, limit: int = 100) -> List[Comment]:
        with self._database.session() as session:
            repo = CommentRepository(session)
            comments = repo.get_published(skip=skip, limit=limit)
            return [Comment.model_validate(c, from_attributes=True) for c in comments]

    async def get_by_id(self, comment_id: int) -> Comment:
        with self._database.session() as session:
            repo = CommentRepository(session)
            comment = repo.get_by_id(comment_id)
            if not comment:
                raise HTTPException(status_code=404, detail="Comment not found")
            return Comment.model_validate(comment, from_attributes=True)

    async def get_by_post(
        self, post_id: int, skip: int = 0, limit: int = 100
    ) -> List[Comment]:
        with self._database.session() as session:
            repo = CommentRepository(session)
            comments = repo.get_by_post(post_id, skip=skip, limit=limit)
            return [Comment.model_validate(c, from_attributes=True) for c in comments]

    async def get_by_author(
        self, author_id: int, skip: int = 0, limit: int = 100
    ) -> List[Comment]:
        with self._database.session() as session:
            repo = CommentRepository(session)
            comments = repo.get_by_author(author_id, skip=skip, limit=limit)
            return [Comment.model_validate(c, from_attributes=True) for c in comments]

    async def update(self, comment_id: int, data: CommentUpdate) -> Comment:
        with self._database.session() as session:
            repo = CommentRepository(session)
            comment = repo.get_by_id(comment_id)
            if not comment:
                raise HTTPException(status_code=404, detail="Comment not found")
            update_dict = {k: v for k, v in data.model_dump().items() if v is not None}
            updated = repo.update(comment, update_dict)
            return Comment.model_validate(updated, from_attributes=True)

    async def delete(self, comment_id: int) -> None:
        with self._database.session() as session:
            repo = CommentRepository(session)
            comment = repo.get_by_id(comment_id)
            if not comment:
                raise HTTPException(status_code=404, detail="Comment not found")
            repo.delete(comment)
