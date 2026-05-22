from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.api.depends import get_user_use_cases
from src.dependencies.auth import get_current_user, get_current_admin_user
from src.domain.user.use_cases.user_use_cases import UserUseCases
from src.schemas.users import User, UserUpdate
from src.schemas.users import User as UserSchema
from src.core.exceptions.api_exceptions import (
    UserNotFoundException,
    UserAlreadyExistsException,
    UserDeletedSuccessfullyException,
    ProfileUpdatedSuccessfullyException,
    InvalidIDException,
)

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
    use_cases: UserUseCases = Depends(get_user_use_cases),
    current_user: UserSchema = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        updated_user = await use_cases.update(db, current_user.id, user_data)
        raise ProfileUpdatedSuccessfullyException(
            user_id=updated_user.id, login=updated_user.login
        )
    except Exception as e:
        raise UserNotFoundException(user_id=current_user.id)


@router.delete("/me")
async def delete_current_user(
    use_cases: UserUseCases = Depends(get_user_use_cases),
    current_user: UserSchema = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        await use_cases.delete(db, current_user.id)
        raise UserDeletedSuccessfullyException(
            user_id=current_user.id, login=current_user.login
        )
    except Exception as e:
        raise UserNotFoundException(user_id=current_user.id)


@router.get("/", response_model=list[User])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    use_cases: UserUseCases = Depends(get_user_use_cases),
    _: UserSchema = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db),
):
    return await use_cases.get_all(db, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=User)
async def get_user(
    user_id: int,
    use_cases: UserUseCases = Depends(get_user_use_cases),
    _: UserSchema = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db),
):
    validate_id(user_id)
    try:
        return await use_cases.get_by_id(db, user_id)
    except Exception as e:
        raise UserNotFoundException(user_id=user_id)


@router.post("/make-admin/{user_id}", response_model=User)
async def make_user_admin(
    user_id: int,
    use_cases: UserUseCases = Depends(get_user_use_cases),
    current_user: UserSchema = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db),
):
    validate_id(user_id)
    try:
        user = await use_cases.get_by_id(db, user_id)
        if not user:
            raise UserNotFoundException(user_id=user_id)
        updated_user = await use_cases.update(db, user_id, UserUpdate(is_admin=True))
        return updated_user
    except Exception as e:
        raise UserNotFoundException(user_id=user_id)


@router.put("/{user_id}", response_model=User)
async def update_user_by_admin(
    user_id: int,
    user_data: UserUpdate,
    use_cases: UserUseCases = Depends(get_user_use_cases),
    _: UserSchema = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db),
):
    validate_id(user_id)
    try:
        updated_user = await use_cases.update(db, user_id, user_data)
        raise ProfileUpdatedSuccessfullyException(
            user_id=updated_user.id, login=updated_user.login
        )
    except Exception as e:
        raise UserNotFoundException(user_id=user_id)


@router.delete("/{user_id}")
async def delete_user_by_admin(
    user_id: int,
    use_cases: UserUseCases = Depends(get_user_use_cases),
    _: UserSchema = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db),
):
    validate_id(user_id)
    try:
        user = await use_cases.get_by_id(db, user_id)
        await use_cases.delete(db, user_id)
        raise UserDeletedSuccessfullyException(user_id=user_id, login=user.login)
    except Exception as e:
        raise UserNotFoundException(user_id=user_id)
