from fastapi import APIRouter, Response
from src.core.database import SessionLocal
from src.domain.auth.use_cases.authenticate_user import AuthenticateUserUseCase
from src.domain.auth.use_cases.register_user import RegisterUserUseCase
from src.domain.auth.use_cases.create_access_token import CreateAccessTokenUseCase
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.core.exceptions.domain_exceptions import (
    UserNotFoundByLoginException, 
    UserLoginIsNotUniqueException
)
from src.core.exceptions.auth_exceptions import InvalidPasswordException
from src.core.exceptions.api_exceptions import (
    UserAlreadyExistsException,
    InvalidCredentialsException,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
def register(login: str, password: str):
    db = SessionLocal()
    try:
        use_case = RegisterUserUseCase()
        user = use_case.execute(db, login, password)
        return {"id": user.id, "login": user.login, "is_admin": user.is_admin}
    except UserLoginIsNotUniqueException:
        raise UserAlreadyExistsException(login=login)
    finally:
        db.close()


@router.post("/login")
def login(login: str, password: str, response: Response):
    db = SessionLocal()
    try:
        auth_use_case = AuthenticateUserUseCase()
        user = auth_use_case.execute(db, login, password)
        
        token_use_case = CreateAccessTokenUseCase()
        access_token = token_use_case.execute(user_id=user.id, login=user.login, is_admin=user.is_admin)
        
        response.set_cookie(
            key="access_token",
            value=f"Bearer {access_token}",
            httponly=True,
            max_age=1800,
        )
        
        return {
            "access_token": access_token, 
            "token_type": "bearer", 
            "user_id": user.id,
            "login": user.login,
            "is_admin": user.is_admin
        }
    except (UserNotFoundByLoginException, InvalidPasswordException):
        raise InvalidCredentialsException()
    finally:
        db.close()


@router.post("/create-admin")
def create_admin(login: str, password: str):
    db = SessionLocal()
    try:
        register_use_case = RegisterUserUseCase()
        user = register_use_case.execute(db, login, password)
        
        user_repo = UserRepository()
        user_repo.update(db, user.id, is_admin=True)
        db.commit()
        
        return {"id": user.id, "login": user.login, "is_admin": True}
    except UserLoginIsNotUniqueException:
        raise UserAlreadyExistsException(login=login)
    finally:
        db.close()