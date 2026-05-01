from fastapi import APIRouter, Depends, HTTPException, status

from src.api.depends import get_post_use_cases
from src.domain.post.use_cases.post_use_cases import PostUseCases
from src.schemas.posts import Post, PostCreate, PostUpdate
from src.core.exceptions.domain_exceptions import (
    PostNotFoundException,
    UserNotFoundByLoginException,
    CategoryNotFoundException,
    LocationNotFoundException,
)

router = APIRouter(prefix="/base", tags=["Base APIs"])


@router.get("/posts", response_model=list[Post])
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
    except PostNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )


@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=Post)
async def create_post(
    post_data: PostCreate,
    use_cases: PostUseCases = Depends(get_post_use_cases),
):
    try:
        return await use_cases.create(post_data)
    except UserNotFoundByLoginException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )
    except (CategoryNotFoundException, LocationNotFoundException) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )


@router.put("/posts/{id}", response_model=Post)
async def update_post(
    id: int,
    post_data: PostUpdate,
    use_cases: PostUseCases = Depends(get_post_use_cases),
):
    try:
        return await use_cases.update(id, post_data)
    except PostNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )
    except (CategoryNotFoundException, LocationNotFoundException) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )


@router.delete("/posts/{id}")
async def delete_post(
    id: int,
    use_cases: PostUseCases = Depends(get_post_use_cases),
):
    try:
        await use_cases.delete(id)
        return {"status": "success", "message": f"Post {id} deleted"}
    except PostNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )
