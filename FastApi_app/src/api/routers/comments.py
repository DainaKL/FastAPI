from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from src.api.depends import get_comment_repository
from src.schemas.comments import Comment, CommentCreate, CommentUpdate
from src.infrastructure.sqlite.repositories.comment_repository import CommentRepository

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.get("/", response_model=List[Comment])
async def get_comments(
    skip: int = 0,
    limit: int = 100,
    repo: CommentRepository = Depends(get_comment_repository)
):
    """Получение списка всех комментариев"""
    try:
        comments = repo.get_all(skip=skip, limit=limit)
        return comments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/published", response_model=List[Comment])
async def get_published_comments(
    skip: int = 0,
    limit: int = 100,
    repo: CommentRepository = Depends(get_comment_repository)
):
    """Получение опубликованных комментариев"""
    try:
        comments = repo.get_published(skip=skip, limit=limit)
        return comments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{comment_id}", response_model=Comment)
async def get_comment(
    comment_id: int,
    repo: CommentRepository = Depends(get_comment_repository)
):
    """Получение комментария по ID"""
    comment = repo.get_by_id(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


@router.get("/post/{post_id}", response_model=List[Comment])
async def get_comments_by_post(
    post_id: int,
    skip: int = 0,
    limit: int = 100,
    repo: CommentRepository = Depends(get_comment_repository)
):
    """Получение комментариев к посту"""
    comments = repo.get_by_post(post_id, skip=skip, limit=limit)
    return comments


@router.get("/author/{author_id}", response_model=List[Comment])
async def get_comments_by_author(
    author_id: int,
    skip: int = 0,
    limit: int = 100,
    repo: CommentRepository = Depends(get_comment_repository)
):
    """Получение комментариев автора"""
    comments = repo.get_by_author(author_id, skip=skip, limit=limit)
    return comments


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Comment)
async def create_comment(
    comment_data: CommentCreate,
    repo: CommentRepository = Depends(get_comment_repository)
):
    """Создание нового комментария"""
    try:
        comment_dict = comment_data.model_dump()
        new_comment = repo.create(**comment_dict)
        return new_comment
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{comment_id}", response_model=Comment)
async def update_comment(
    comment_id: int,
    comment_data: CommentUpdate,
    repo: CommentRepository = Depends(get_comment_repository)
):
    """Обновление комментария"""
    try:
        update_dict = {k: v for k, v in comment_data.model_dump().items() if v is not None}
        updated = repo.update(comment_id, **update_dict)
        if not updated:
            raise HTTPException(status_code=404, detail="Comment not found")
        return updated
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{comment_id}")
async def delete_comment(
    comment_id: int,
    repo: CommentRepository = Depends(get_comment_repository)
):
    """Удаление комментария"""
    deleted = repo.delete(comment_id)
    try:
        if not deleted:
            raise HTTPException(status_code=404, detail="Comment not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))