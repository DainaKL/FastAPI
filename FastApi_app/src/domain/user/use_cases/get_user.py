from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.schemas.users import User as UserSchema
from src.core.exceptions.api_exceptions import UserNotFoundException


class GetUserUseCase:
    def __init__(self):
        self._repo = UserRepository()

    async def execute(self, db: AsyncSession, user_id: int) -> UserSchema:
        user = await self._repo.get_by_id(db, user_id)
        if not user:
            raise UserNotFoundException(user_id=user_id)
        return UserSchema.model_validate(user)
