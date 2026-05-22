from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.security import decode_access_token
from src.core.database import get_db
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.core.exceptions.api_exceptions import (
    InvalidTokenException,
    UserNotFoundException,
    AdminRequiredException,
)
from src.schemas.users import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token", auto_error=False)


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
) -> User:
    if not token:
        raise InvalidTokenException()

    payload = decode_access_token(token)

    if not payload:
        raise InvalidTokenException()

    user_id = payload.get("sub")
    login = payload.get("login")

    if not user_id or not login:
        raise InvalidTokenException()

    user_repo = UserRepository()
    user = await user_repo.get_by_id(db, int(user_id))

    if not user:
        raise UserNotFoundException(user_id=user_id)

    return User.model_validate(user)


async def get_current_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_admin:
        raise AdminRequiredException()
    return current_user
