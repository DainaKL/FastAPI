from fastapi import APIRouter, Depends, HTTPException, status

from src.api.depends import get_user_use_cases
from src.domain.user.use_cases.user_use_cases import UserUseCases
from src.schemas.users import User, UserCreate, UserUpdate
from src.core.exceptions.domain_exceptions import (
    UserNotFoundByLoginException,
    UserLoginIsNotUniqueException,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[User])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    use_cases: UserUseCases = Depends(get_user_use_cases),
):
    return await use_cases.get_all(skip=skip, limit=limit)


@router.get("/{user_id}", response_model=User)
async def get_user(
    user_id: int,
    use_cases: UserUseCases = Depends(get_user_use_cases),
):
    try:
        return await use_cases.get_by_id(user_id)
    except UserNotFoundByLoginException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )


@router.get("/login/{login}", response_model=User)
async def get_user_by_login(
    login: str,
    use_cases: UserUseCases = Depends(get_user_use_cases),
):
    try:
        return await use_cases.get_by_login(login)
    except UserNotFoundByLoginException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(
    user_data: UserCreate,
    use_cases: UserUseCases = Depends(get_user_use_cases),
):
    try:
        return await use_cases.create(user_data)
    except UserLoginIsNotUniqueException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.get_detail())


@router.put("/{user_id}", response_model=User)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    use_cases: UserUseCases = Depends(get_user_use_cases),
):
    try:
        return await use_cases.update(user_id, user_data)
    except UserNotFoundByLoginException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    use_cases: UserUseCases = Depends(get_user_use_cases),
):
    try:
        await use_cases.delete(user_id)
        return {"status": "success", "message": f"User {user_id} deleted"}
    except UserNotFoundByLoginException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )
