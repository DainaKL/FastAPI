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
from src.services.media_uploader import save_file

router = APIRouter(prefix="/posts", tags=["Posts"])


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
    from src.infrastructure.sqlite.repositories.post_repository import PostRepository

    repo = PostRepository(db)
    post = await repo.get_by_id(post_id)
    if post.author_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Вы не можете добавить картинку к чужому посту"
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
    from src.infrastructure.sqlite.repositories.post_repository import PostRepository

    repo = PostRepository(db)
    post = await repo.get_by_id(post_id)
    if post.author_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=403, detail="Вы не можете удалять картинки из чужого поста"
        )

    image = await repo.get_image_by_id(image_id)
    if not image or image.post_id != post_id:
        raise HTTPException(status_code=404, detail="Image not found")

    await repo.delete_image(image_id)
    await db.commit()
    return {"message": "Image deleted", "image_id": image_id}
