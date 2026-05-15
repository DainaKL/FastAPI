from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from src.core.config import settings
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.core.exceptions.api_exceptions import CredentialsException
import logging
logger = logging.getLogger(__name__)

security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_AUTH_KEY.get_secret_value(),
            algorithms=[settings.AUTH_ALGORITHM],
        )
    except JWTError as e:
        raise CredentialsException(detail=f"JWT error: {str(e)}")
    
    user_id = payload.get("sub")
    login = payload.get("login")
    if not user_id or not login:
        raise CredentialsException(detail="Missing sub or login in token")
    
    with database.session() as session:
        repo = UserRepository()
        user = repo.get_by_id(session=session, user_id=int(user_id))
        if not user:
            raise CredentialsException(detail="User not found")
        # Сохраняем значения внутри сессии
        user_id_value = user.id
        user_login_value = user.login
    
    return {"id": user_id_value, "login": user_login_value}


def get_user_use_cases():
    from src.domain.user.use_cases.user_use_cases import UserUseCases
    return UserUseCases()


def get_post_use_cases():
    from src.domain.post.use_cases.post_use_cases import PostUseCases
    return PostUseCases()


def get_comment_use_cases():
    from src.domain.comment.use_cases.comment_use_cases import CommentUseCases
    return CommentUseCases()


def get_category_use_cases():
    from src.domain.category.use_cases.category_use_cases import CategoryUseCases
    return CategoryUseCases()


def get_location_use_cases():
    from src.domain.location.use_cases.location_use_cases import LocationUseCases
    return LocationUseCases()