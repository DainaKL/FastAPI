from src.domain.user.use_cases.get_users import GetUsersUseCase
from src.domain.user.use_cases.get_user import GetUserUseCase
from src.domain.user.use_cases.create_user import CreateUserUseCase
from src.domain.user.use_cases.update_user import UpdateUserUseCase
from src.domain.user.use_cases.delete_user import DeleteUserUseCase


def get_user_use_cases():
    return {
        "get_all": GetUsersUseCase(),
        "get_by_id": GetUserUseCase(),
        "create": CreateUserUseCase(),
        "update": UpdateUserUseCase(),
        "delete": DeleteUserUseCase(),
    }
