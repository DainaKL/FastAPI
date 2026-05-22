from datetime import datetime
from fastapi import APIRouter, Depends, status, UploadFile, File
from pathlib import Path

from src.api.depends import (
    get_get_posts_use_case,
    get_get_post_use_case,
    get_get_post_by_id_use_case,
    get_create_post_use_case,
    get_update_post_use_case,
    get_delete_post_use_case,
)
from src.dependencies.auth import get_current_user
from src.domain.post.use_cases.get_posts import GetPostsUseCase
from src.domain.post.use_cases.get_post import GetPostUseCase
from src.domain.post.use_cases.get_post_by_id import GetPostByIdUseCase
from src.domain.post.use_cases.create_post import CreatePostUseCase
from src.domain.post.use_cases.update_post import UpdatePostUseCase
from src.domain.post.use_cases.delete_post import DeletePostUseCase
from src.schemas.posts import Post, PostCreate, PostUpdate
from src.core.exceptions.api_exceptions import (
    NotFoundException,
    PostForbiddenException,
    PostAuthRequiredException,
)
from src.core.exceptions.domain_exceptions import (
    PostNotFoundException,
    CategoryNotFoundException,
    LocationNotFoundException,
)

router = APIRouter(prefix="/base", tags=["Base APIs"])


@router.get("/posts", response_model=list[Post])
async def get_posts(
    skip: int = 0,
    limit: int = 100,
    use_case: GetPostsUseCase = Depends(get_get_posts_use_case),
):
    return await use_case.execute(skip=skip, limit=limit)


@router.get("/posts/{id}", response_model=Post)
async def get_post(
    id: int,
    use_case: GetPostUseCase = Depends(get_get_post_use_case),
):
    try:
        return await use_case.execute(post_id=id)
    except PostNotFoundException as e:
        raise NotFoundException(detail=e.get_detail())


@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=Post)
async def create_post(
    post_data: PostCreate,
    use_case: CreatePostUseCase = Depends(get_create_post_use_case),
    current_user: dict = Depends(get_current_user),
):
    try:
        post_data.author_id = current_user["id"]
        return await use_case.execute(post_data=post_data)
    except (CategoryNotFoundException, LocationNotFoundException) as e:
        raise NotFoundException(detail=e.get_detail())


@router.put("/posts/{id}", response_model=Post)
async def update_post(
    id: int,
    post_data: PostUpdate,
    get_post_use_case: GetPostByIdUseCase = Depends(get_get_post_by_id_use_case),
    update_use_case: UpdatePostUseCase = Depends(get_update_post_use_case),
    current_user: dict = Depends(get_current_user),
):
    try:
        post = await get_post_use_case.execute(post_id=id)
        if not current_user.get("is_admin") and post.author_id != current_user["id"]:
            raise PostForbiddenException(action="редактировать")
        
        return await update_use_case.execute(post_id=id, data=post_data)
    except PostNotFoundException as e:
        raise NotFoundException(detail=e.get_detail())
    except (CategoryNotFoundException, LocationNotFoundException) as e:
        raise NotFoundException(detail=e.get_detail())


@router.delete("/posts/{id}")
async def delete_post(
    id: int,
    get_post_use_case: GetPostByIdUseCase = Depends(get_get_post_by_id_use_case),
    delete_use_case: DeletePostUseCase = Depends(get_delete_post_use_case),
    current_user: dict = Depends(get_current_user),
):
    try:
        post = await get_post_use_case.execute(post_id=id)
        if not current_user.get("is_admin") and post.author_id != current_user["id"]:
            raise PostForbiddenException(action="удалять")
        
        await delete_use_case.execute(post_id=id)
        return {"status": "success", "message": f"Post {id} deleted"}
    except PostNotFoundException as e:
        raise NotFoundException(detail=e.get_detail())


@router.post("/posts/{id}/image", response_model=Post)
async def upload_post_image(
    id: int,
    image: UploadFile = File(...),
    get_post_use_case: GetPostByIdUseCase = Depends(get_get_post_by_id_use_case),
    update_use_case: UpdatePostUseCase = Depends(get_update_post_use_case),
    current_user: dict = Depends(get_current_user),
):
    if not current_user:
        raise PostAuthRequiredException()
    
    try:
        post = await get_post_use_case.execute(post_id=id)
        if not current_user.get("is_admin") and post.author_id != current_user["id"]:
            raise PostForbiddenException(action="редактировать")
        
        media_dir = Path("media/post_images")
        media_dir.mkdir(parents=True, exist_ok=True)

        file_extension = Path(image.filename).suffix
        file_name = f"{id}_{datetime.now().timestamp()}{file_extension}"
        file_path = media_dir / file_name

        with open(file_path, "wb") as buffer:
            content = await image.read()
            buffer.write(content)

        image_url = f"/media/post_images/{file_name}"
        updated_post = await update_use_case.execute(
            post_id=id, data=PostUpdate(image=image_url)
        )
        return updated_post
    except PostNotFoundException as e:
        raise NotFoundException(detail=e.get_detail())