import hashlib
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.depends import get_user_repository
from src.infrastructure.sqlite.repositories.user_repository import \
    UserRepository
from src.schemas.users import User, UserCreate, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[User])
async def get_users(
    skip: int = 0, limit: int = 100, repo: UserRepository = Depends(get_user_repository)
):
    users = repo.get_all(skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int, repo: UserRepository = Depends(get_user_repository)):
    user = repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/login/{login}", response_model=User)
async def get_user_by_login(
    login: str, repo: UserRepository = Depends(get_user_repository)
):
    user = repo.get_by_login(login)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(
    user_data: UserCreate, repo: UserRepository = Depends(get_user_repository)
):
    # Проверка на существующего пользователя
    if repo.get_by_login(user_data.login):
        raise HTTPException(status_code=400, detail="Login already exists")

    # Хеширование пароля
    hashed_password = hashlib.sha256(user_data.password.encode()).hexdigest()

    new_user = repo.create(login=user_data.login, password=hashed_password)
    return new_user


@router.put("/{user_id}", response_model=User)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    repo: UserRepository = Depends(get_user_repository),
):
    update_dict = {k: v for k, v in user_data.model_dump().items() if v is not None}
    if "password" in update_dict:
        update_dict["password"] = hashlib.sha256(
            update_dict["password"].encode()
        ).hexdigest()
    updated = repo.update(user_id, **update_dict)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated


@router.delete("/{user_id}")
async def delete_user(
    user_id: int, repo: UserRepository = Depends(get_user_repository)
):
    deleted = repo.delete(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}
