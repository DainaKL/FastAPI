from fastapi import APIRouter, Depends
from src.api.depends import get_user_use_cases
from src.dependencies.auth import get_current_user, get_current_admin_user
from src.domain.user.use_cases.user_use_cases import UserUseCases
from src.schemas.users import User, UserUpdate
from src.core.exceptions.api_exceptions import (
    UserNotFoundException,
    UserAlreadyExistsException,
    UserDeletedSuccessfullyException,
    ProfileUpdatedSuccessfullyException,
)
from src.core.exceptions.domain_exceptions import (
    UserNotFoundByIdException,
    UserLoginIsNotUniqueException,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=User)
def get_current_user_info(
    current_user: dict = Depends(get_current_user)
):
    return User(id=current_user["id"], login=current_user["login"])


@router.put("/me")
def update_current_user(
    user_data: UserUpdate,
    use_cases: UserUseCases = Depends(get_user_use_cases),
    current_user: dict = Depends(get_current_user),
):
    try:
        updated_user = use_cases.update(current_user["id"], user_data)
        raise ProfileUpdatedSuccessfullyException(
            user_id=updated_user.id,
            login=updated_user.login
        )
    except UserNotFoundByIdException:
        raise UserNotFoundException(user_id=current_user["id"])
    except UserLoginIsNotUniqueException as e:
        login = str(e).split("'")[1] if "'" in str(e) else "unknown"
        raise UserAlreadyExistsException(login=login)


@router.delete("/me")
def delete_current_user(
    use_cases: UserUseCases = Depends(get_user_use_cases),
    current_user: dict = Depends(get_current_user),
):
    try:
        use_cases.delete(current_user["id"])
        raise UserDeletedSuccessfullyException(
            user_id=current_user["id"],
            login=current_user["login"]
        )
    except UserNotFoundByIdException:
        raise UserNotFoundException(user_id=current_user["id"])


@router.get("/", response_model=list[User])
def get_users(
    skip: int = 0,
    limit: int = 100,
    use_cases: UserUseCases = Depends(get_user_use_cases),
    current_user: dict = Depends(get_current_admin_user),
):
    return use_cases.get_all(skip=skip, limit=limit)


@router.get("/{user_id}", response_model=User)
def get_user(
    user_id: int,
    use_cases: UserUseCases = Depends(get_user_use_cases),
    current_user: dict = Depends(get_current_admin_user),
):
    try:
        return use_cases.get_by_id(user_id)
    except UserNotFoundByIdException:
        raise UserNotFoundException(user_id=user_id)


@router.put("/{user_id}")
def update_user_by_admin(
    user_id: int,
    user_data: UserUpdate,
    use_cases: UserUseCases = Depends(get_user_use_cases),
    current_user: dict = Depends(get_current_admin_user),
):
    try:
        updated_user = use_cases.update(user_id, user_data)
        raise ProfileUpdatedSuccessfullyException(
            user_id=updated_user.id,
            login=updated_user.login
        )
    except UserNotFoundByIdException:
        raise UserNotFoundException(user_id=user_id)
    except UserLoginIsNotUniqueException as e:
        login = str(e).split("'")[1] if "'" in str(e) else "unknown"
        raise UserAlreadyExistsException(login=login)


@router.delete("/{user_id}")
def delete_user_by_admin(
    user_id: int,
    use_cases: UserUseCases = Depends(get_user_use_cases),
    current_user: dict = Depends(get_current_admin_user),
):
    try:
        user = use_cases.get_by_id(user_id)
        use_cases.delete(user_id)
        raise UserDeletedSuccessfullyException(
            user_id=user_id,
            login=user.login
        )
    except UserNotFoundByIdException:
        raise UserNotFoundException(user_id=user_id)