import logging
from typing import List, Optional
from fastapi import UploadFile, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.postgres.repositories.comment_repository import CommentRepository
from src.infrastructure.postgres.repositories.post_repository import PostRepository
from src.infrastructure.postgres.repositories.user_repository import UserRepository
from src.infrastructure.postgres.models.comment import Comment
from src.schemas.comments import Comment as CommentSchema
from src.core.exceptions.api_exceptions import PostNotFoundException, UserNotFoundException, InvalidIDException
from src.services.media_uploader import save_file

logger = logging.getLogger(__name__)


class CreateCommentUseCase:
    async def execute(
        self,
        db: AsyncSession,
        text: str,
        post_id: int,
        is_published: bool,
        author_id: int,
        images: List[UploadFile] = None
    ) -> CommentSchema:
        try:
            if author_id <= 0:
                raise InvalidIDException(author_id)
            if post_id <= 0:
                raise InvalidIDException(post_id)
            
            user_repo = UserRepository(db)
            user = await user_repo.get_by_id(author_id)
            if not user:
                raise UserNotFoundException(user_id=author_id)
            
            post_repo = PostRepository(db)
            post = await post_repo.get_by_id(post_id)
            if not post:
                raise PostNotFoundException(post_id=post_id)
            
            comment_repo = CommentRepository(db)
            comment = await comment_repo.create(
                text=text,
                post_id=post_id,
                author_id=author_id,
                is_published=is_published
            )
            
            if images:
                for image in images:
                    # Сохраняем изображение комментария
                    url = await save_file(image, entity_type='comment')
                    await comment_repo.add_image(comment.id, url)
            
            await db.commit()
            
            # Загружаем комментарий с картинками
            stmt = select(Comment).where(Comment.id == comment.id).options(selectinload(Comment.images))
            result = await db.execute(stmt)
            comment_with_images = result.unique().scalar_one()
            
            return CommentSchema.model_validate(comment_with_images)
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in create comment: {e}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка при создании комментария: {str(e)}"
            )
