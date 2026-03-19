from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.users import UserRepository
from schemas.users import User as UserSchema
from core.exceptions.database_exceptions import UserNotFoundException
from core.exceptions.domain_exceptions import UserNotFoundByLoginException


class GetUserByLoginUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, login: str) -> UserSchema:
        try:
            with self._database.session() as session:
                user = self._repo.get(session=session, login=login)
        except UserNotFoundException:
            raise UserNotFoundByLoginException(login=login)

        return UserSchema.model_validate(obj=user)
