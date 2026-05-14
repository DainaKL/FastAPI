from typing import Annotated
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Column, Integer, String

from src.core.config import settings
from src.core.database import get_async_session, Base
from src.core.security import verify_password, get_password_hash
from src.schemas.auth import LoginResponse
from src.core.exceptions.api_exceptions import CredentialsException
from src.core.exceptions.domain_exceptions import UserNotFoundByLoginException
from src.core.exceptions.auth_exceptions import InvalidPasswordException

router = APIRouter(prefix="/auth", tags=["Authentication"])


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}
    
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(50), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)


@router.post("/token", response_model=LoginResponse)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_async_session),
) -> LoginResponse:
    try:
        result = await db.execute(
            select(User).where(User.login == form_data.username)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            raise UserNotFoundByLoginException(form_data.username)
        
        if not verify_password(form_data.password, user.password):
            raise InvalidPasswordException()
            
    except UserNotFoundByLoginException as e:
        raise CredentialsException(detail=e.get_detail())
    except InvalidPasswordException as e:
        raise CredentialsException(detail=e.get_detail())
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {"sub": str(user.id), "login": user.login}
    
    to_encode = token_data.copy()
    if access_token_expires:
        expire = datetime.now(timezone.utc) + access_token_expires
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    access_token = jwt.encode(
        claims=to_encode,
        key=settings.SECRET_AUTH_KEY.get_secret_value(),
        algorithm=settings.AUTH_ALGORITHM,
    )
    
    return LoginResponse(
        access_token=access_token,
        user_id=user.id,
        login=user.login,
    )


@router.post("/register")
async def register(
    login: str,
    password: str,
    db: AsyncSession = Depends(get_async_session),
):
    result = await db.execute(select(User).where(User.login == login))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Пользователь уже существует")
    
    user = User(login=login, password=get_password_hash(password))
    db.add(user)
    await db.commit()
    
    return {"message": "Пользователь создан"}