from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.schemas.users import User as UserSchema
from src.core.exceptions.domain_exceptions import UserNotFoundByLoginException


class GetUserByLoginUseCase:
    def __init__(self) -> None:
        self._repo = UserRepository()

    async def execute(self, db: AsyncSession, login: str) -> UserSchema:
        user = await self._repo.get_by_login(db, login)
        if not user:
            raise UserNotFoundByLoginException(login=login)
        return UserSchema.model_validate(user)
