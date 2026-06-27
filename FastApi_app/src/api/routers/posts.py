from datetime import datetime as dt
from typing import List, Optional
from fastapi import APIRouter, Depends, status, UploadFile, File, Form, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.dependencies.auth import get_current_user
from src.schemas.posts import Post, PostCreate, PostUpdate
from src.schemas.users import User
from src.domain.post.use_cases.create_post import CreatePostUseCase
from src.domain.post.use_cases.get_posts import GetPostsUseCase
from src.domain.post.use_cases.get_post import GetPostUseCase
from src.domain.post.use_cases.update_post import UpdatePostUseCase
from src.domain.post.use_cases.delete_post import DeletePostUseCase
from src.infrastructure.postgres.repositories.post_repository import PostRepository
from src.infrastructure.postgres.repositories.post_image_repository import (
    PostImageRepository,
)
from src.services.media_uploader import save_file
from src.core.exceptions.api_exceptions import (
    NotFoundException,
    ForbiddenException,
    InvalidIDException,
)
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/posts", tags=["Posts"])


def validate_id(id: int) -> int:
    if id <= 0:
        raise InvalidIDException(id)
    return id


@router.get("/", response_model=List[Post])
async def get_posts(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    use_case = GetPostsUseCase()
    return await use_case.execute(db, skip=skip, limit=limit)


@router.get("/{id}", response_model=Post)
async def get_post(
    id: int,
    db: AsyncSession = Depends(get_db),
):
    validate_id(id)
    use_case = GetPostUseCase()
    return await use_case.execute(db, id)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
async def create_post(
    title: str = Form(...),
    text: str = Form(...),
    is_published: bool = Form(True),
    location_id: Optional[int] = Form(None),
    category_id: Optional[int] = Form(None),
    images: List[UploadFile] = File([]),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post_data = PostCreate(
        title=title,
        text=text,
        is_published=is_published,
        location_id=location_id if location_id and location_id > 0 else None,
        category_id=category_id if category_id and category_id > 0 else None,
    )

    use_case = CreatePostUseCase()
    result = await use_case.execute(db, post_data, current_user.id, images)
    await db.commit()
    return result


@router.put("/{id}", response_model=Post)
async def update_post(
    id: int,
    post_data: PostUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    validate_id(id)
    use_case = UpdatePostUseCase()
    return await use_case.execute(
        db, id, post_data, current_user.id, current_user.is_admin
    )


@router.delete("/{id}")
async def delete_post(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    validate_id(id)
    use_case = DeletePostUseCase()
    await use_case.execute(db, id, current_user.id, current_user.is_admin)
    return {"status": "success", "message": f"Post {id} deleted"}


@router.post("/{post_id}/images/")
async def add_post_image(
    post_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    validate_id(post_id)

    repo = PostRepository(db)
    post = await repo.get_by_id(post_id)
    if not post:
        raise NotFoundException(detail=f"Пост с id '{post_id}' не найден")

    if not current_user.is_admin and post.author_id != current_user.id:
        raise ForbiddenException(
            detail="Вы не можете добавлять картинки к чужому посту"
        )

    url = await save_file(file)
    await repo.add_image(post_id, url)
    await db.commit()

    return {"message": "Image added", "url": url, "post_id": post_id}


@router.delete("/{post_id}/images/{image_id}")
async def delete_post_image(
    post_id: int,
    image_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    validate_id(post_id)
    validate_id(image_id)

    repo = PostRepository(db)
    post = await repo.get_by_id(post_id)
    if not post:
        raise NotFoundException(detail=f"Пост с id '{post_id}' не найден")

    if not current_user.is_admin and post.author_id != current_user.id:
        raise ForbiddenException(detail="Вы не можете удалять картинки из чужого поста")

    image_repo = PostImageRepository(db)
    deleted = await image_repo.delete_by_id(image_id)

    if not deleted:
        raise NotFoundException(detail=f"Картинка с id '{image_id}' не найдена")

    await db.commit()
    return {"status": "success", "message": f"Картинка {image_id} удалена"}
