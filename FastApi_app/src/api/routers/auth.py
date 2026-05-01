from fastapi import APIRouter, HTTPException, status
from src.domain.auth.use_cases.authenticate_user import AuthenticateUserUseCase
from src.domain.auth.use_cases.create_access_token import CreateAccessTokenUseCase
from src.schemas.auth import LoginRequest, LoginResponse
from src.core.exceptions.domain_exceptions import UserNotFoundByLoginException
from src.core.exceptions.auth_exceptions import InvalidPasswordException

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=LoginResponse)
async def login(login_data: LoginRequest):
    try:
        user_data = await AuthenticateUserUseCase().execute(
            login_data.login, login_data.password
        )
        access_token = await CreateAccessTokenUseCase().execute(user_data["login"])

        return LoginResponse(
            access_token=access_token,
            token_type="bearer",
            user_id=user_data["id"],
            login=user_data["login"],
        )
    except UserNotFoundByLoginException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=e.get_detail()
        )
    except InvalidPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=e.get_detail()
        )
