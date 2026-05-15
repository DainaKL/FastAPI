import logging
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.core.database import SessionLocal
from src.core.exceptions.domain_exceptions import UserNotFoundByIdException

logger = logging.getLogger(__name__)


class DeleteUserUseCase:
    def __init__(self):
        self._repo = UserRepository()

    def execute(self, user_id: int) -> None:
        db = SessionLocal()
        try:
            user = self._repo.get_by_id(db, user_id)
            if not user:
                raise UserNotFoundByIdException(user_id)

            self._repo.delete(db, user_id)
            db.commit()
        finally:
            db.close()
