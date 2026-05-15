from src.domain.user.use_cases.get_users import GetUsersUseCase
from src.domain.user.use_cases.get_user import GetUserUseCase
from src.domain.user.use_cases.create_user import CreateUserUseCase
from src.domain.user.use_cases.update_user import UpdateUserUseCase
from src.domain.user.use_cases.delete_user import DeleteUserUseCase


class UserUseCases:
    def __init__(self):
        self._get_all = GetUsersUseCase()
        self._get_by_id = GetUserUseCase()
        self._create = CreateUserUseCase()
        self._update = UpdateUserUseCase()
        self._delete = DeleteUserUseCase()

    def get_all(self, skip: int = 0, limit: int = 100):
        return self._get_all.execute(skip=skip, limit=limit)

    def get_by_id(self, user_id: int):
        return self._get_by_id.execute(user_id)

    def create(self, login: str, password: str):
        return self._create.execute(login, password)

    def update(self, user_id: int, user_data):
        return self._update.execute(user_id, user_data)

    def delete(self, user_id: int):
        return self._delete.execute(user_id)
