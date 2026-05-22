from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.api.depends import get_comment_use_cases
from src.dependencies.auth import get_current_user
from src.domain.comment.use_cases.comment_use_cases import CommentUseCases
from src.schemas.comments import Comment, CommentCreate, CommentUpdate
from src.schemas.users import User
from src.core.exceptions.api_exceptions import (
    NotFoundException,
    CommentForbiddenException,
    InvalidIDException,
)

router = APIRouter(prefix="/comments", tags=["Comments"])


def validate_id(id: int) -> int:
    if id <= 0:
        raise InvalidIDException(id)
    return id


@router.get("/", response_model=list[Comment])
async def get_comments(
    skip: int = 0,
    limit: int = 100,
    use_cases: CommentUseCases = Depends(get_comment_use_cases),
    db: AsyncSession = Depends(get_db),
):
    return await use_cases.get_all(db, skip=skip, limit=limit)


@router.get("/published", response_model=list[Comment])
async def get_published_comments(
    skip: int = 0,
    limit: int = 100,
    use_cases: CommentUseCases = Depends(get_comment_use_cases),
    db: AsyncSession = Depends(get_db),
):
    return await use_cases.get_published(db, skip=skip, limit=limit)


@router.get("/{comment_id}", response_model=Comment)
async def get_comment(
    comment_id: int,
    use_cases: CommentUseCases = Depends(get_comment_use_cases),
    db: AsyncSession = Depends(get_db),
):
    validate_id(comment_id)
    try:
        return await use_cases.get_by_id(db, comment_id)
    except Exception as e:
        raise NotFoundException(detail=str(e))


@router.get("/post/{post_id}", response_model=list[Comment])
async def get_comments_by_post(
    post_id: int,
    skip: int = 0,
    limit: int = 100,
    use_cases: CommentUseCases = Depends(get_comment_use_cases),
    db: AsyncSession = Depends(get_db),
):
    validate_id(post_id)
    return await use_cases.get_by_post(db, post_id, skip=skip, limit=limit)


@router.get("/author/{author_id}", response_model=list[Comment])
async def get_comments_by_author(
    author_id: int,
    skip: int = 0,
    limit: int = 100,
    use_cases: CommentUseCases = Depends(get_comment_use_cases),
    db: AsyncSession = Depends(get_db),
):
    validate_id(author_id)
    return await use_cases.get_by_author(db, author_id, skip=skip, limit=limit)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Comment)
async def create_comment(
    comment_data: CommentCreate,
    use_cases: CommentUseCases = Depends(get_comment_use_cases),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    comment_data.author_id = current_user.id
    return await use_cases.create(db, comment_data)


@router.put("/{comment_id}", response_model=Comment)
async def update_comment(
    comment_id: int,
    comment_data: CommentUpdate,
    use_cases: CommentUseCases = Depends(get_comment_use_cases),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    validate_id(comment_id)
    comment = await use_cases.get_by_id(db, comment_id)
    if not current_user.is_admin and comment.author_id != current_user.id:
        raise CommentForbiddenException(action="редактировать")
    return await use_cases.update(db, comment_id, comment_data)


@router.delete("/{comment_id}")
async def delete_comment(
    comment_id: int,
    use_cases: CommentUseCases = Depends(get_comment_use_cases),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    validate_id(comment_id)
    comment = await use_cases.get_by_id(db, comment_id)
    if not current_user.is_admin and comment.author_id != current_user.id:
        raise CommentForbiddenException(action="удалять")
    await use_cases.delete(db, comment_id)
    return {"status": "success", "message": f"Comment {comment_id} deleted"}
