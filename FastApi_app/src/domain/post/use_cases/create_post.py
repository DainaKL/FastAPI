from datetime import datetime
from typing import List, Optional
from fastapi import UploadFile
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.sqlite.repositories.post_repository import PostRepository
from src.infrastructure.sqlite.repositories.category_repository import (
    CategoryRepository,
)
from src.infrastructure.sqlite.repositories.location_repository import (
    LocationRepository,
)
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.schemas.posts import Post as PostSchema, PostCreate
from src.core.exceptions.api_exceptions import (
    CategoryNotFoundException,
    LocationNotFoundException,
    UserNotFoundException,
    InvalidIDException,
)
from src.services.media_uploader import save_file


class CreatePostUseCase:
    async def execute(
        self,
        db: AsyncSession,
        post_data: PostCreate,
        author_id: int,
        images: List[UploadFile] = None,
    ):
        if author_id <= 0:
            raise InvalidIDException(author_id)

        user_repo = UserRepository(db)
        user = await user_repo.get_by_id(author_id)
        if not user:
            raise UserNotFoundException(user_id=author_id)

        if post_data.category_id is not None:
            if post_data.category_id <= 0:
                raise InvalidIDException(post_data.category_id)
            cat_repo = CategoryRepository(db)
            category = await cat_repo.get_by_id(post_data.category_id)
            if not category:
                raise CategoryNotFoundException(category_id=post_data.category_id)
        else:
            post_data.category_id = None

        if post_data.location_id is not None:
            if post_data.location_id <= 0:
                raise InvalidIDException(post_data.location_id)
            loc_repo = LocationRepository(db)
            location = await loc_repo.get_by_id(post_data.location_id)
            if not location:
                raise LocationNotFoundException(location_id=post_data.location_id)
        else:
            post_data.location_id = None

        if post_data.pub_date is None:
            post_data.pub_date = datetime.now()

        post_repo = PostRepository(db)
        post = await post_repo.create(
            title=post_data.title,
            text=post_data.text,
            pub_date=post_data.pub_date,
            is_published=post_data.is_published,
            author_id=author_id,
            location_id=post_data.location_id,
            category_id=post_data.category_id,
        )

        if images:
            for image in images:
                url = await save_file(image)
                await post_repo.add_image(post.id, url)

        stmt = (
            select(post_repo.model)
            .where(post_repo.model.id == post.id)
            .options(selectinload(post_repo.model.images))
        )
        result = await db.execute(stmt)
        post_with_images = result.unique().scalar_one()

        await db.commit()
        return PostSchema.model_validate(post_with_images)
