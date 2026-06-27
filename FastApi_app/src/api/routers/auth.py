from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.domain.auth.use_cases.authenticate_user import AuthenticateUserUseCase
from src.domain.auth.use_cases.register_user import RegisterUserUseCase
from src.domain.auth.use_cases.create_access_token import CreateAccessTokenUseCase
from src.schemas.users import UserCreate, UserResponse
from src.core.exceptions.api_exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
    InvalidPasswordException,
)


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        use_case = RegisterUserUseCase()
        user = await use_case.execute(db, user_data.login, user_data.password)
        return UserResponse.model_validate(user)
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/token")
async def token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    try:
        use_case = AuthenticateUserUseCase()
        user = await use_case.execute(db, form_data.username, form_data.password)

        token_use_case = CreateAccessTokenUseCase()
        access_token = token_use_case.execute(
            user_id=user.id, login=user.login, is_admin=user.is_admin
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь с таким логином не найден",
        )
    except InvalidPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный пароль"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Ошибка авторизации"
        )
