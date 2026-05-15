import logging
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.core.database import SessionLocal
from src.core.exceptions.domain_exceptions import UserNotFoundByLoginException

logger = logging.getLogger(__name__)


class DeleteUserUseCase:
    def __init__(self) -> None:
        self._repo = UserRepository()

    async def execute(self, user_id: int) -> None:
        db = SessionLocal()
        try:
            user = self._repo.get_by_id(db, user_id)
            if not user:
                raise UserNotFoundByLoginException(login=str(user_id))
            
            deleted = self._repo.delete(db, user_id)
            db.commit()
            if not deleted:
                raise UserNotFoundByLoginException(login=str(user_id))
        finally:
            db.close()