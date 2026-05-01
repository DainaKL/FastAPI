from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.core.security import verify_password
from src.core.exceptions.domain_exceptions import UserNotFoundByLoginException
from src.core.exceptions.auth_exceptions import InvalidPasswordException


class AuthenticateUserUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = UserRepository()

    async def execute(self, login: str, password: str):
        with self._database.session() as session:
            user = self._repo.get_by_login(session=session, login=login)
            if not user:
                raise UserNotFoundByLoginException(login=login)

            if not verify_password(password, user.password):
                raise InvalidPasswordException()

            user_id = user.id
            user_login = user.login

        return {"id": user_id, "login": user_login}
