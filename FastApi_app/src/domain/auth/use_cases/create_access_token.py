from src.core.security import create_access_token
from src.core.config import settings


class CreateAccessTokenUseCase:
    def execute(self, user_id: int, login: str, is_admin: bool) -> str:
        return create_access_token(
            data={"sub": str(user_id), "login": login, "is_admin": is_admin}
        )
