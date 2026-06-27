import logging
from typing import List, Optional
from fastapi import UploadFile, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import ValidationError

from src.infrastructure.postgres.repositories.post_repository import PostRepository
from src.infrastructure.postgres.repositories.category_repository import CategoryRepository
from src.infrastructure.postgres.repositories.location_repository import LocationRepository
from src.infrastructure.postgres.repositories.user_repository import UserRepository
from src.infrastructure.postgres.models.post import Post
from src.infrastructure.postgres.models.user import User
from src.schemas.posts import PostCreate
from src.schemas.posts import Post as PostSchema
from src.core.exceptions.api_exceptions import CategoryNotFoundException, LocationNotFoundException, UserNotFoundException, InvalidIDException
from src.services.media_uploader import save_file

logger = logging.getLogger(__name__)


class CreatePostUseCase:
    async def execute(
        self,
        db: AsyncSession,
        post_data: PostCreate,
        author_id: int,
        images: List[UploadFile] = None
    ) -> PostSchema:
        try:
            if author_id <= 0:
                raise InvalidIDException(author_id)
            
            user_repo = UserRepository(db)
            user = await user_repo.get_by_id(author_id)
            if not user:
                raise UserNotFoundException(user_id=author_id)
            
            if post_data.category_id:
                category_repo = CategoryRepository(db)
                category = await category_repo.get_by_id(post_data.category_id)
                if not category:
                    raise CategoryNotFoundException(category_id=post_data.category_id)
            
            if post_data.location_id:
                location_repo = LocationRepository(db)
                location = await location_repo.get_by_id(post_data.location_id)
                if not location:
                    raise LocationNotFoundException(location_id=post_data.location_id)
            
            post_repo = PostRepository(db)
            post = await post_repo.create(
                title=post_data.title,
                text=post_data.text,
                author_id=author_id,
                category_id=post_data.category_id,
                location_id=post_data.location_id,
                is_published=post_data.is_published
            )
            
            if images:
                for image in images:
                    url = await save_file(image, entity_type='post')
                    await post_repo.add_image(post.id, url)
            
            await db.commit()
            
            stmt = (
                select(Post)
                .where(Post.id == post.id)
                .options(
                    selectinload(Post.author).selectinload(User.images),
                    selectinload(Post.images),
                    selectinload(Post.category),
                    selectinload(Post.location)
                )
            )
            result = await db.execute(stmt)
            post_with_data = result.unique().scalar_one()
            
            return PostSchema.model_validate(post_with_data)
            
        except ValidationError as e:
            errors = []
            for error in e.errors():
                field = '.'.join(str(loc) for loc in error.get('loc', ['unknown']))
                msg = error.get('msg', 'Unknown error')
                errors.append(f"{field}: {msg}")
            
            error_detail = "; ".join(errors)
            logger.error(f"Validation error: {error_detail}")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Ошибка валидации: {error_detail}"
            )
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error in create post: {e}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Внутренняя ошибка сервера: {str(e)}"
            )
