from src.core.security import create_access_token


class CreateAccessTokenUseCase:
    async def execute(self, login: str) -> str:
        return create_access_token(data={"sub": login})
