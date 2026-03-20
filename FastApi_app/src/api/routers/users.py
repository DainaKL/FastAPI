from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from src.api.depends import get_user_repository
from src.schemas.users import User, UserCreate, UserUpdate
from src.infrastructure.sqlite.repositories.user_repository import UserRepository

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[User])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    repo: UserRepository = Depends(get_user_repository)
):
    """Получение списка всех пользователей"""
    users = repo.get_all(skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=User)
async def get_user(
    user_id: int,
    repo: UserRepository = Depends(get_user_repository)
):
    """Получение пользователя по ID"""
    user = repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/username/{username}", response_model=User)
async def get_user_by_username(
    username: str,
    repo: UserRepository = Depends(get_user_repository)
):
    """Получение пользователя по имени"""
    user = repo.get_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(
    user_data: UserCreate,
    repo: UserRepository = Depends(get_user_repository)
):
    """Создание нового пользователя"""
    # Проверка на существующего пользователя
    if repo.get_by_username(user_data.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    if repo.get_by_email(user_data.email):
        raise HTTPException(status_code=400, detail="Email already exists")
    
    # Хеширование пароля (временно, лучше использовать passlib)
    import hashlib
    user_data.password = hashlib.sha256(user_data.password.encode()).hexdigest()
    
    user_dict = user_data.model_dump()
    new_user = repo.create(**user_dict)
    return new_user


@router.put("/{user_id}", response_model=User)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    repo: UserRepository = Depends(get_user_repository)
):
    """Обновление пользователя"""
    update_dict = {k: v for k, v in user_data.model_dump().items() if v is not None}
    updated = repo.update(user_id, **update_dict)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    repo: UserRepository = Depends(get_user_repository)
):
    """Удаление пользователя"""
    deleted = repo.delete(user_id)
    try:
        if not deleted:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    