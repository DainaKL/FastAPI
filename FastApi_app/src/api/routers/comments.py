from typing import List, Optional
from fastapi import APIRouter, Depends, status, UploadFile, File, Form, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.dependencies.auth import get_current_user
from src.schemas.comments import Comment, CommentUpdate
from src.schemas.users import User
from src.infrastructure.sqlite.repositories.comment_repository import CommentRepository
from src.domain.comment.use_cases.create_comment import CreateCommentUseCase
from src.domain.comment.use_cases.get_comments import GetCommentsUseCase
from src.domain.comment.use_cases.get_comment import GetCommentUseCase
from src.domain.comment.use_cases.update_comment import UpdateCommentUseCase
from src.domain.comment.use_cases.delete_comment import DeleteCommentUseCase

router = APIRouter(prefix="/comments", tags=["Comments"])


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
    use_case = GetCommentUseCase()
    return await use_case.execute(db, id)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Comment)
async def create_comment(
    text: str = Form(...),
    post_id: int = Form(...),
    is_published: bool = Form(True),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    use_case = CreateCommentUseCase()
    result = await use_case.execute(db, text, post_id, is_published, current_user.id)
    await db.commit()
    return result


@router.put("/{id}", response_model=Comment)
async def update_comment(
    id: int,
    comment_data: CommentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
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
    use_case = DeleteCommentUseCase()
    await use_case.execute(db, id, current_user.id, current_user.is_admin)
    return {"status": "success", "message": f"Comment {id} deleted"}
