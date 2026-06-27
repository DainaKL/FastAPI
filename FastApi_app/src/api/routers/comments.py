from typing import List, Optional
from fastapi import APIRouter, Depends, status, UploadFile, File, Form, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.dependencies.auth import get_current_user
from src.schemas.comments import Comment, CommentUpdate
from src.schemas.users import User
from src.infrastructure.postgres.repositories.comment_repository import (
    CommentRepository,
)
from src.infrastructure.postgres.repositories.comment_image_repository import (
    CommentImageRepository,
)
from src.domain.comment.use_cases.create_comment import CreateCommentUseCase
from src.domain.comment.use_cases.get_comments import GetCommentsUseCase
from src.domain.comment.use_cases.get_comment import GetCommentUseCase
from src.domain.comment.use_cases.update_comment import UpdateCommentUseCase
from src.domain.comment.use_cases.delete_comment import DeleteCommentUseCase
from src.services.media_uploader import save_file
from src.core.exceptions.api_exceptions import (
    NotFoundException,
    ForbiddenException,
    InvalidIDException,
)
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/comments", tags=["Comments"])


def validate_id(id: int) -> int:
    if id <= 0:
        raise InvalidIDException(id)
    return id


@router.get("/", response_model=List[Comment])
async def get_comments(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    use_case = GetCommentsUseCase()
    return await use_case.execute(db, skip=skip, limit=limit)


@router.get("/{id}", response_model=Comment)
async def get_comment(
    id: int,
    db: AsyncSession = Depends(get_db),
):
    validate_id(id)
    use_case = GetCommentUseCase()
    return await use_case.execute(db, id)


@router.get("/post/{post_id}", response_model=List[Comment])
async def get_comments_by_post(
    post_id: int,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    validate_id(post_id)
    use_case = GetCommentsUseCase()
    return await use_case.execute(db, skip=skip, limit=limit, post_id=post_id)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Comment)
async def create_comment(
    text: str = Form(...),
    post_id: int = Form(...),
    is_published: bool = Form(True),
    images: List[UploadFile] = File([]),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    use_case = CreateCommentUseCase()
    result = await use_case.execute(
        db, text, post_id, is_published, current_user.id, images
    )
    await db.commit()
    return result


@router.put("/{id}", response_model=Comment)
async def update_comment(
    id: int,
    comment_data: CommentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    validate_id(id)
    use_case = UpdateCommentUseCase()
    return await use_case.execute(
        db, id, comment_data, current_user.id, current_user.is_admin
    )


@router.delete("/{id}")
async def delete_comment(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    validate_id(id)
    use_case = DeleteCommentUseCase()
    await use_case.execute(db, id, current_user.id, current_user.is_admin)
    return {"status": "success", "message": f"Comment {id} deleted"}


@router.post("/{comment_id}/images/")
async def add_comment_image(
    comment_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    validate_id(comment_id)

    repo = CommentRepository(db)
    comment = await repo.get_by_id(comment_id)
    if not comment:
        raise NotFoundException(detail=f"Комментарий с id '{comment_id}' не найден")

    if not current_user.is_admin and comment.author_id != current_user.id:
        raise ForbiddenException(
            detail="Вы не можете добавлять картинки к чужому комментарию"
        )

    url = await save_file(file)
    await repo.add_image(comment_id, url)
    await db.commit()

    return {"message": "Image added", "url": url, "comment_id": comment_id}


@router.delete("/{comment_id}/images/{image_id}")
async def delete_comment_image(
    comment_id: int,
    image_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    validate_id(comment_id)
    validate_id(image_id)

    repo = CommentRepository(db)
    comment = await repo.get_by_id(comment_id)
    if not comment:
        raise NotFoundException(detail=f"Комментарий с id '{comment_id}' не найден")

    if not current_user.is_admin and comment.author_id != current_user.id:
        raise ForbiddenException(
            detail="Вы не можете удалять картинки из чужого комментария"
        )

    image_repo = CommentImageRepository(db)
    deleted = await image_repo.delete_by_id(image_id)

    if not deleted:
        raise NotFoundException(detail=f"Картинка с id '{image_id}' не найдена")

    await db.commit()
    return {"status": "success", "message": f"Картинка {image_id} удалена"}
