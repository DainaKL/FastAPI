from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.schemas.users import User as UserSchema
from src.core.database import SessionLocal
from src.core.exceptions.domain_exceptions import UserNotFoundByIdException


class GetUserUseCase:
    def __init__(self):
        self._repo = UserRepository()

    def execute(self, user_id: int) -> UserSchema:
        db = SessionLocal()
        try:
            user = self._repo.get_by_id(db, user_id)
            if not user:
                raise UserNotFoundByIdException(user_id)
            return UserSchema.model_validate(user, from_attributes=True)
        finally:
            db.close()