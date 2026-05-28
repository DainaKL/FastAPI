from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.dependencies.auth import get_current_user, get_current_admin_user
from src.schemas.users import User, UserUpdate
from src.schemas.users import User as UserSchema
from src.core.exceptions.api_exceptions import (
    UserNotFoundException,
    InvalidIDException,
    ForbiddenException,
)
from src.domain.user.use_cases.get_users import GetUsersUseCase
from src.domain.user.use_cases.get_user import GetUserUseCase
from src.domain.user.use_cases.update_user import UpdateUserUseCase
from src.domain.user.use_cases.delete_user import DeleteUserUseCase

router = APIRouter(prefix="/users", tags=["Users"])


def validate_id(id: int) -> int:
    if id <= 0:
        raise InvalidIDException(id)
    return id


@router.get("/me", response_model=User)
async def get_current_user_info(current_user: UserSchema = Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=User)
async def update_current_user(
    user_data: UserUpdate,
    current_user: UserSchema = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    use_case = UpdateUserUseCase()
    updated_user = await use_case.execute(
        db, current_user.id, user_data, current_user.id, current_user.is_admin
    )
    return updated_user


@router.delete("/me")
async def delete_current_user(
    current_user: UserSchema = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    use_case = DeleteUserUseCase()
    await use_case.execute(db, current_user.id, current_user.id, current_user.is_admin)
    return {"status": "success", "message": "Пользователь удален"}


@router.get("/", response_model=list[User])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    current_user: UserSchema = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db),
):
    use_case = GetUsersUseCase()
    return await use_case.execute(db, skip=skip, limit=limit, is_admin=True)


@router.get("/{user_id}", response_model=User)
async def get_user(
    user_id: int,
    current_user: UserSchema = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db),
):
    validate_id(user_id)
    use_case = GetUserUseCase()
    return await use_case.execute(db, user_id)


@router.post("/make-admin/{user_id}", response_model=User)
async def make_user_admin(
    user_id: int,
    current_user: UserSchema = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db),
):
    validate_id(user_id)
    use_case = UpdateUserUseCase()
    updated_user = await use_case.execute(
        db, user_id, UserUpdate(is_admin=True), current_user.id, True
    )
    return updated_user


@router.put("/{user_id}", response_model=User)
async def update_user_by_admin(
    user_id: int,
    user_data: UserUpdate,
    current_user: UserSchema = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db),
):
    validate_id(user_id)
    use_case = UpdateUserUseCase()
    updated_user = await use_case.execute(db, user_id, user_data, current_user.id, True)
    return updated_user


@router.delete("/{user_id}")
async def delete_user_by_admin(
    user_id: int,
    current_user: UserSchema = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db),
):
    validate_id(user_id)
    use_case = DeleteUserUseCase()
    await use_case.execute(db, user_id, current_user.id, True)
    return {"status": "success", "message": f"Пользователь {user_id} удален"}
