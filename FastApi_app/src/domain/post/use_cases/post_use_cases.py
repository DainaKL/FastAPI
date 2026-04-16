from typing import List

from fastapi import HTTPException

from src.core.exceptions.database_exceptions import (
    DatabaseOperationException, PostNotFoundException)
from src.core.exceptions.domain_exceptions import \
    PostNotFoundException as DomainPostNotFoundException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.post_repository import \
    PostRepository
from src.schemas.posts import Post, PostCreate, PostUpdate


class PostUseCases:
    def __init__(self):
        self._database = database

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Post]:
        with self._database.session() as session:
            repo = PostRepository(session)
            try:
                posts = repo.get_all(skip=skip, limit=limit)
                return [Post.model_validate(p, from_attributes=True) for p in posts]
            except DatabaseOperationException as e:
                raise HTTPException(status_code=500, detail=e.get_detail())

    async def get_by_id(self, post_id: int) -> Post:
        with self._database.session() as session:
            repo = PostRepository(session)
            try:
                post = repo.get_by_id(post_id)
                return Post.model_validate(post, from_attributes=True)
            except PostNotFoundException:
                raise DomainPostNotFoundException(post_id=post_id)
            except DatabaseOperationException as e:
                raise HTTPException(status_code=500, detail=e.get_detail())

    async def create(self, data: PostCreate) -> Post:
        with self._database.session() as session:
            repo = PostRepository(session)
            try:
                post_dict = data.model_dump()
                post = repo.create(**post_dict)
                return Post.model_validate(post, from_attributes=True)
            except DatabaseOperationException as e:
                raise HTTPException(status_code=500, detail=e.get_detail())

    async def update(self, post_id: int, data: PostUpdate) -> Post:
        with self._database.session() as session:
            repo = PostRepository(session)
            try:
                update_dict = {
                    k: v for k, v in data.model_dump().items() if v is not None
                }
                post = repo.update(post_id, **update_dict)
                return Post.model_validate(post, from_attributes=True)
            except PostNotFoundException:
                raise DomainPostNotFoundException(post_id=post_id)
            except DatabaseOperationException as e:
                raise HTTPException(status_code=500, detail=e.get_detail())

    async def delete(self, post_id: int) -> None:
        with self._database.session() as session:
            repo = PostRepository(session)
            try:
                repo.delete(post_id)
            except PostNotFoundException:
                raise DomainPostNotFoundException(post_id=post_id)
            except DatabaseOperationException as e:
                raise HTTPException(status_code=500, detail=e.get_detail())
