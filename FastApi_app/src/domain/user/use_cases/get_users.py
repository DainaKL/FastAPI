from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.schemas.users import User as UserSchema
from src.core.database import SessionLocal
from typing import List


class GetUsersUseCase:
    def __init__(self):
        self._repo = UserRepository()

    def execute(self, skip: int = 0, limit: int = 100) -> List[UserSchema]:
        db = SessionLocal()
        try:
            users = self._repo.get_all(db, skip=skip, limit=limit)
            return [UserSchema.model_validate(user, from_attributes=True) for user in users]
        finally:
            db.close()