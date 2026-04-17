from src.domain.user.use_cases.get_users import GetUsersUseCase
from src.domain.user.use_cases.get_user import GetUserUseCase
from src.domain.user.use_cases.get_user_by_login import GetUserByLoginUseCase
from src.domain.user.use_cases.create_user import CreateUserUseCase
from src.domain.user.use_cases.update_user import UpdateUserUseCase
from src.domain.user.use_cases.delete_user import DeleteUserUseCase


class UserUseCases:
    def __init__(self):
        self.get_all = GetUsersUseCase().execute
        self.get_by_id = GetUserUseCase().execute
        self.get_by_login = GetUserByLoginUseCase().execute
        self.create = CreateUserUseCase().execute
        self.update = UpdateUserUseCase().execute
        self.delete = DeleteUserUseCase().execute
