from datetime import datetime
from fastapi import APIRouter, Depends, status, UploadFile, File, HTTPException
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.api.depends import (
    get_get_posts_use_case,
    get_get_post_use_case,
    get_create_post_use_case,
    get_update_post_use_case,
    get_delete_post_use_case,
)
from src.dependencies.auth import get_current_user
from src.domain.post.use_cases.get_posts import GetPostsUseCase
from src.domain.post.use_cases.get_post import GetPostUseCase
from src.domain.post.use_cases.create_post import CreatePostUseCase
from src.domain.post.use_cases.update_post import UpdatePostUseCase
from src.domain.post.use_cases.delete_post import DeletePostUseCase
from src.schemas.posts import Post, PostCreate, PostUpdate
from src.schemas.users import User
from src.core.exceptions.api_exceptions import (
    NotFoundException,
    PostForbiddenException,
    PostAuthRequiredException,
    InvalidIDException,
)
from src.core.exceptions.domain_exceptions import CategoryNotFoundException, LocationNotFoundException, UserNotFoundByIdException
from src.infrastructure.sqlite.repositories.post_repository import PostRepository

router = APIRouter(prefix="/base", tags=["Base APIs"])


def validate_id(id: int) -> int:
    if id <= 0:
        raise InvalidIDException(id)
    return id


@router.get("/posts", response_model=list[Post])
async def get_posts(
    skip: int = 0,
    limit: int = 100,
    use_case: GetPostsUseCase = Depends(get_get_posts_use_case),
    db: AsyncSession = Depends(get_db),
):
    return await use_case.execute(db, skip=skip, limit=limit)


@router.get("/posts/{id}", response_model=Post)
async def get_post(
    id: int,
    use_case: GetPostUseCase = Depends(get_get_post_use_case),
    db: AsyncSession = Depends(get_db),
):
    validate_id(id)
    try:
        return await use_case.execute(db, id)
    except Exception as e:
        raise NotFoundException(detail=str(e))


@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=Post)
async def create_post(
    post_data: PostCreate,
    use_case: CreatePostUseCase = Depends(get_create_post_use_case),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    post_data.author_id = current_user.id
    try:
        result = await use_case.execute(db, post_data)
        await db.commit()
        return result
    except (CategoryNotFoundException, LocationNotFoundException, UserNotFoundByIdException) as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/posts/{id}", response_model=Post)
async def update_post(
    id: int,
    post_data: PostUpdate,
    use_case: UpdatePostUseCase = Depends(get_update_post_use_case),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    validate_id(id)
    repo = PostRepository()
    post = await repo.get_by_id(db, id)
    if not post:
        raise NotFoundException(detail=f"Post {id} not found")
    if not current_user.is_admin and post.author_id != current_user.id:
        raise PostForbiddenException(action="редактировать")
    result = await use_case.execute(db, id, post_data)
    await db.commit()
    return result


@router.delete("/posts/{id}")
async def delete_post(
    id: int,
    use_case: DeletePostUseCase = Depends(get_delete_post_use_case),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    validate_id(id)
    repo = PostRepository()
    post = await repo.get_by_id(db, id)
    
    if not post:
        raise NotFoundException(detail=f"Post {id} not found")
    
    if not current_user.is_admin and post.author_id != current_user.id:
        raise PostForbiddenException(action="удалять")
    
    await use_case.execute(db, id)
    await db.commit()
    return {"status": "success", "message": f"Post {id} deleted"}


@router.post("/posts/{post_id}/image", response_model=Post)
async def upload_post_image(
    post_id: int,
    image: UploadFile = File(...),
    get_post_use_case: GetPostUseCase = Depends(get_get_post_use_case),
    update_use_case: UpdatePostUseCase = Depends(get_update_post_use_case),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    validate_id(post_id)
    if not current_user:
        raise PostAuthRequiredException()

    post = await get_post_use_case.execute(db, post_id)
    if not current_user.is_admin and post.author_id != current_user.id:
        raise PostForbiddenException(action="редактировать")

    media_dir = Path("media/post_images")
    media_dir.mkdir(parents=True, exist_ok=True)

    file_extension = Path(image.filename).suffix
    file_name = f"{post_id}_{datetime.now().timestamp()}{file_extension}"
    file_path = media_dir / file_name

    with open(file_path, "wb") as buffer:
        content = await image.read()
        buffer.write(content)

    image_url = f"/media/post_images/{file_name}"
    result = await update_use_case.execute(db, post_id, PostUpdate(image=image_url))
    await db.commit()
    return result
