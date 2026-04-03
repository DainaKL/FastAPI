from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from src.api.depends import get_comment_use_cases
from src.domain.comment.use_cases.comment_use_cases import CommentUseCases
from src.schemas.comments import Comment, CommentCreate, CommentUpdate

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.get("/", response_model=List[Comment])
async def get_comments(
    skip: int = 0,
    limit: int = 100,
    use_cases: CommentUseCases = Depends(get_comment_use_cases),
):
    return await use_cases.get_all(skip=skip, limit=limit)


@router.get("/published", response_model=List[Comment])
async def get_published_comments(
    skip: int = 0,
    limit: int = 100,
    use_cases: CommentUseCases = Depends(get_comment_use_cases),
):
    return await use_cases.get_published(skip=skip, limit=limit)


@router.get("/{comment_id}", response_model=Comment)
async def get_comment(
    comment_id: int,
    use_cases: CommentUseCases = Depends(get_comment_use_cases),
):
    try:
        return await use_cases.get_by_id(comment_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Comment not found")


@router.get("/post/{post_id}", response_model=List[Comment])
async def get_comments_by_post(
    post_id: int,
    skip: int = 0,
    limit: int = 100,
    use_cases: CommentUseCases = Depends(get_comment_use_cases),
):
    return await use_cases.get_by_post(post_id, skip=skip, limit=limit)


@router.get("/author/{author_id}", response_model=List[Comment])
async def get_comments_by_author(
    author_id: int,
    skip: int = 0,
    limit: int = 100,
    use_cases: CommentUseCases = Depends(get_comment_use_cases),
):
    return await use_cases.get_by_author(author_id, skip=skip, limit=limit)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Comment)
async def create_comment(
    comment_data: CommentCreate,
    use_cases: CommentUseCases = Depends(get_comment_use_cases),
):
    return await use_cases.create(comment_data)


@router.put("/{comment_id}", response_model=Comment)
async def update_comment(
    comment_id: int,
    comment_data: CommentUpdate,
    use_cases: CommentUseCases = Depends(get_comment_use_cases),
):
    try:
        return await use_cases.update(comment_id, comment_data)
    except ValueError:
        raise HTTPException(status_code=404, detail="Comment not found")


@router.delete("/{comment_id}")
async def delete_comment(
    comment_id: int,
    use_cases: CommentUseCases = Depends(get_comment_use_cases),
):
    try:
        await use_cases.delete(comment_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Comment not found")
