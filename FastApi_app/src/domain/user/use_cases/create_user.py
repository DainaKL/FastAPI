from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.users import UserRepository
from schemas.users import User as UserSchema, CreateUser
from core.exceptions.database_exceptions import UserAlreadyExistsException
from core.exceptions.domain_exceptions import UserLoginIsNotUniqueException


class CreateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user: CreateUser) -> UserSchema:
        try:
            with self._database.session() as session:
                user = self._repo.create(session=session, user=user)
        except UserAlreadyExistsException:
            raise UserLoginIsNotUniqueException(login=user.login)

        return UserSchema.model_validate(obj=user)
