import logging
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.schemas.users import User as UserSchema, UserUpdate
from src.core.exceptions.api_exceptions import (
    UserNotFoundException,
    UserAlreadyExistsException,
    ForbiddenException,
    InvalidIDException,
)
from src.core.security import get_password_hash

logger = logging.getLogger(__name__)


class UpdateUserUseCase:
    async def execute(
        self,
        db: AsyncSession,
        user_id: int,
        data: UserUpdate,
        current_user_id: int,
        is_admin: bool,
    ):
        if user_id <= 0:
            raise InvalidIDException(user_id)

        repo = UserRepository(db)
        existing_user = await repo.get_by_id(user_id)
        if not existing_user:
            raise UserNotFoundException(user_id=user_id)

        if not is_admin and current_user_id != user_id:
            raise ForbiddenException(
                detail="Вы можете редактировать только свой профиль"
            )

        if data.login and data.login != existing_user.login:
            if await repo.exists_by_login(data.login):
                raise UserAlreadyExistsException(login=data.login)

        update_dict = {}
        if data.login:
            update_dict["login"] = data.login
        if data.password:
            update_dict["password"] = get_password_hash(data.password)
        if data.is_admin is not None and is_admin:
            update_dict["is_admin"] = data.is_admin

        if update_dict:
            user = await repo.update(user_id, **update_dict)
            await db.commit()
        else:
            user = existing_user

        return UserSchema.model_validate(user)
