from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.core.security import decode_access_token
from src.core.database import SessionLocal
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.core.exceptions.api_exceptions import (
    InvalidTokenException,
    UserNotFoundException,
    AdminRequiredException,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)

    if not payload:
        raise InvalidTokenException()

    user_id = payload.get("sub")
    login = payload.get("login")

    if not user_id or not login:
        raise InvalidTokenException()

    db = SessionLocal()
    try:
        user_repo = UserRepository()
        user = user_repo.get_by_id(db, int(user_id))

        if not user:
            raise UserNotFoundException(user_id=user_id)

        return {"id": user.id, "login": user.login, "is_admin": user.is_admin}
    finally:
        db.close()


def get_current_admin_user(current_user: dict = Depends(get_current_user)):
    if not current_user.get("is_admin", False):
        raise AdminRequiredException()
    return current_user