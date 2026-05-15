from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.infrastructure.sqlite.models.users import User as UserModel
from src.core.security import (
    get_password_hash,
    create_access_token,
    decode_access_token,
)
from src.schemas.auth import LoginRequest, LoginResponse
from src.domain.auth.use_cases.authenticate_user import AuthenticateUserUseCase
from src.core.exceptions.domain_exceptions import UserNotFoundByLoginException
from src.core.exceptions.auth_exceptions import InvalidPasswordException
from src.core.exceptions.api_exceptions import CredentialsException

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()


@router.post("/login", response_model=LoginResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    try:
        user = AuthenticateUserUseCase().execute(
            db, login_data.login, login_data.password
        )
        access_token = create_access_token(
            data={"sub": str(user.id), "login": user.login}
        )

        return LoginResponse(
            access_token=access_token,
            token_type="bearer",
            user_id=user.id,
            login=user.login,
        )
    except (UserNotFoundByLoginException, InvalidPasswordException) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=e.get_detail()
        )


@router.post("/register")
async def register(login: str, password: str, db: Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter(UserModel.login == login).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = get_password_hash(password)
    new_user = UserModel(login=login, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created", "user_id": new_user.id, "login": new_user.login}


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = decode_access_token(token)

    if not payload:
        raise CredentialsException()

    user_id = payload.get("sub")
    login = payload.get("login")

    if not user_id or not login:
        raise CredentialsException()

    return {"id": int(user_id), "login": login}
