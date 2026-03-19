from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.depends import get_post_repository
from src.schemas.posts import Post, PostCreate, PostUpdate
from src.infrastructure.sqlite.repositories.post_repository import PostRepository


router = APIRouter(prefix="/base", tags=["Base APIs"])

# GET запрос для получения списка всех постов с пагинацией
@router.get("/posts", response_model=List[Post])
async def get_posts(
    skip: int = 0, 
    limit: int = 100,
    post_repo: PostRepository = Depends(get_post_repository)
):
    # Получение списка всех постов из репозитория
    try:
        posts = post_repo.get_all(skip=skip, limit=limit)
        return posts
    except Exception as e:
        print(f"Error in get_posts: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# GET запрос для получения конкретного поста по ID
@router.get("/posts/{id}", response_model=Post)
async def get_post(
    id: int,
    post_repo: PostRepository = Depends(get_post_repository)
):
    # Получение поста по ID из репозитория
    try:
        post = post_repo.get_by_id(id)
        # Если пост не найден, возвращаем 404 ошибку
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return post
    except Exception as e:
        print(f"Error in get_post: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# POST запрос для создания нового поста
@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=Post)
async def create_post(
    post_data: PostCreate,
    post_repo: PostRepository = Depends(get_post_repository)
):
    # Создание нового поста в базе данных
    try:
        # Преобразуем Pydantic модель в словарь для передачи в репозиторий
        post_dict = post_data.model_dump()
        new_post = post_repo.create(**post_dict)
        # Проверяем успешность создания
        if not new_post:
            raise HTTPException(status_code=500, detail="Failed to create post")
        return new_post
    except Exception as e:
        print(f"Error in create_post: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# PUT запрос для обновления существующего поста
@router.put("/posts/{id}", response_model=Post)
async def update_post(
    id: int, 
    post_data: PostUpdate,
    post_repo: PostRepository = Depends(get_post_repository)
):
    # Обновление существующего поста
    try:
        # Убираем поля со значением None, оставляем только те, что нужно обновить
        update_dict = {k: v for k, v in post_data.model_dump().items() if v is not None}
        updated_post = post_repo.update(id, **update_dict)
        # Если пост не найден, возвращаем 404 ошибку
        if not updated_post:
            raise HTTPException(status_code=404, detail="Post not found")
        return updated_post
    except Exception as e:
        print(f"Error in update_post: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# DELETE запрос для удаления поста
@router.delete("/posts/{id}")
async def delete_post(
    id: int,
    post_repo: PostRepository = Depends(get_post_repository)
):
    # Удаление поста из базы данных
    try:
        deleted_post = post_repo.delete(id)
        # Если пост не найден, возвращаем 404 ошибку
        if not deleted_post:
            raise HTTPException(status_code=404, detail="Post not found")
        return {"message": "Post deleted successfully"}
    except Exception as e:
        print(f"Error in delete_post: {e}")
        raise HTTPException(status_code=500, detail=str(e))
