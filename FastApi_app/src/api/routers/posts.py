from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from src.api.depends import get_post_use_cases
from src.domain.post.use_cases.post_use_cases import PostUseCases
from src.schemas.posts import Post, PostCreate, PostUpdate

router = APIRouter(prefix="/base", tags=["Base APIs"])


@router.get("/posts", response_model=List[Post])
async def get_posts(
    skip: int = 0,
    limit: int = 100,
    use_cases: PostUseCases = Depends(get_post_use_cases),
):
    return await use_cases.get_all(skip=skip, limit=limit)


@router.get("/posts/{id}", response_model=Post)
async def get_post(
    id: int,
    use_cases: PostUseCases = Depends(get_post_use_cases),
):
    try:
        return await use_cases.get_by_id(id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Post not found")


@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=Post)
async def create_post(
    post_data: PostCreate,
    use_cases: PostUseCases = Depends(get_post_use_cases),
):
    return await use_cases.create(post_data)


@router.put("/posts/{id}", response_model=Post)
async def update_post(
    id: int,
    post_data: PostUpdate,
    use_cases: PostUseCases = Depends(get_post_use_cases),
):
    try:
        return await use_cases.update(id, post_data)
    except ValueError:
        raise HTTPException(status_code=404, detail="Post not found")


@router.delete("/posts/{id}")
async def delete_post(
    id: int,
    use_cases: PostUseCases = Depends(get_post_use_cases),
):
    try:
        await use_cases.delete(id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Post not found")
