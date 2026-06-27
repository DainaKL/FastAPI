from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.security import decode_access_token
from src.core.database import get_db
from src.infrastructure.postgres.models.user import User
from src.core.exceptions.api_exceptions import (
    InvalidTokenException,
    UserNotFoundException,
    AdminRequiredException,
)
from src.schemas.users import User as UserSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token", auto_error=False)


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
) -> UserSchema:
    if not token:
        raise InvalidTokenException()

    payload = decode_access_token(token)

    if not payload:
        raise InvalidTokenException()

    user_id = payload.get("sub")
    login = payload.get("login")

    if not user_id or not login:
        raise InvalidTokenException()

    stmt = (
        select(User).where(User.id == int(user_id)).options(selectinload(User.images))
    )
    result = await db.execute(stmt)
    user = result.unique().scalar_one_or_none()

    if not user:
        raise UserNotFoundException(user_id=user_id)

    return UserSchema.model_validate(user)


async def get_current_admin_user(
    current_user: UserSchema = Depends(get_current_user),
) -> UserSchema:
    if not current_user.is_admin:
        raise AdminRequiredException()
    return current_user
