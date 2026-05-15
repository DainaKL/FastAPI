import logging
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.schemas.users import User as UserSchema, UserUpdate
from src.core.database import SessionLocal
from src.core.exceptions.domain_exceptions import (
    UserNotFoundByIdException,
    UserLoginIsNotUniqueException,
)

logger = logging.getLogger(__name__)


class UpdateUserUseCase:
    def __init__(self):
        self._repo = UserRepository()

    def execute(self, user_id: int, data: UserUpdate) -> UserSchema:
        db = SessionLocal()
        try:
            existing_user = self._repo.get_by_id(db, user_id)
            if not existing_user:
                raise UserNotFoundByIdException(user_id)

            if data.login and data.login != existing_user.login:
                if self._repo.exists_by_login(db, data.login):
                    raise UserLoginIsNotUniqueException(login=data.login)

            update_dict = {}
            if data.login:
                update_dict["login"] = data.login
            if data.password:
                update_dict["password"] = data.password

            if update_dict:
                user = self._repo.update(db, user_id, **update_dict)
                db.commit()
            else:
                user = existing_user

            return UserSchema.model_validate(user, from_attributes=True)
        finally:
            db.close()
