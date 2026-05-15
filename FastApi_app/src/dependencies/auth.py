from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from src.core.security import decode_access_token

security = HTTPBearer()


async def get_current_user(credentials: Depends(security)):
    token = credentials.credentials
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный токен",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    login = payload.get("login")

    if not user_id or not login:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный формат токена",
        )

    return {"id": int(user_id), "login": login}
