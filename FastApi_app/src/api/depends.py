from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.core.security import decode_access_token
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.core.exceptions.api_exceptions import CredentialsException

security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = decode_access_token(token)
    
    if not payload:
        raise CredentialsException()
    
    user_id = payload.get("sub")
    login = payload.get("login")
    
    if not user_id or not login:
        raise CredentialsException()
    
    with database.session() as session:
        repo = UserRepository()
        user = repo.get_by_id(session=session, user_id=int(user_id))
        if not user:
            raise CredentialsException()
    
    return {"id": user.id, "login": user.login}


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