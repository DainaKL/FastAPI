import logging
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.schemas.users import User as UserSchema
from src.core.database import SessionLocal

logger = logging.getLogger(__name__)


class GetUsersUseCase:
    def __init__(self) -> None:
        self._repo = UserRepository()

    async def execute(self, skip: int = 0, limit: int = 100):
        db = SessionLocal()
        try:
            users = self._repo.get_all(db, skip=skip, limit=limit)
            return [UserSchema.model_validate(u, from_attributes=True) for u in users]
        finally:
            db.close()