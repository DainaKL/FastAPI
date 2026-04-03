from fastapi import HTTPException, status
from typing import List
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.post_repository import PostRepository
from src.infrastructure.sqlite.models.post import Post as PostModel
from src.schemas.posts import PostCreate, PostUpdate, Post


class PostUseCases:
    def __init__(self):
        self._database = database

    async def create(self, data: PostCreate) -> Post:
        with self._database.session() as session:
            repo = PostRepository(session)
            post = PostModel(**data.model_dump())
            created = repo.create(post)
            return Post.model_validate(created, from_attributes=True)

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Post]:
        with self._database.session() as session:
            repo = PostRepository(session)
            posts = repo.get_all(skip=skip, limit=limit)
            return [Post.model_validate(p, from_attributes=True) for p in posts]

    async def get_by_id(self, post_id: int) -> Post:
        with self._database.session() as session:
            repo = PostRepository(session)
            post = repo.get_by_id(post_id)
            if not post:
                raise HTTPException(status_code=404, detail="Post not found")
            return Post.model_validate(post, from_attributes=True)

    async def update(self, post_id: int, data: PostUpdate) -> Post:
        with self._database.session() as session:
            repo = PostRepository(session)
            post = repo.get_by_id(post_id)
            if not post:
                raise HTTPException(status_code=404, detail="Post not found")
            update_dict = {k: v for k, v in data.model_dump().items() if v is not None}
            updated = repo.update(post, update_dict)
            return Post.model_validate(updated, from_attributes=True)

    async def delete(self, post_id: int) -> None:
        with self._database.session() as session:
            repo = PostRepository(session)
            post = repo.get_by_id(post_id)
            if not post:
                raise HTTPException(status_code=404, detail="Post not found")
            repo.delete(post)
