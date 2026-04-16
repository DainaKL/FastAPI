from src.core.exceptions.base_exceptions import BaseDatabaseException


class UserNotFoundException(BaseDatabaseException):
    def __init__(self, login: str = None, user_id: int = None) -> None:
        detail = "Пользователь не найден"
        if login:
            detail = f"Пользователь с логином {login} не найден"
        if user_id:
            detail = f"Пользователь с id {user_id} не найден"
        super().__init__(detail=detail)


class UserAlreadyExistsException(BaseDatabaseException):
    def __init__(self, login: str) -> None:
        detail = f"Пользователь с логином {login} уже существует"
        super().__init__(detail=detail)


class PostNotFoundException(BaseDatabaseException):
    def __init__(self, post_id: int) -> None:
        detail = f"Пост с id {post_id} не найден"
        super().__init__(detail=detail)


class CommentNotFoundException(BaseDatabaseException):
    def __init__(self, comment_id: int) -> None:
        detail = f"Комментарий с id {comment_id} не найден"
        super().__init__(detail=detail)


class CategoryNotFoundException(BaseDatabaseException):
    def __init__(self, category_id: int = None, slug: str = None) -> None:
        detail = "Категория не найдена"
        if category_id:
            detail = f"Категория с id {category_id} не найдена"
        if slug:
            detail = f"Категория с slug {slug} не найдена"
        super().__init__(detail=detail)


class LocationNotFoundException(BaseDatabaseException):
    def __init__(self, location_id: int = None, name: str = None) -> None:
        detail = "Локация не найдена"
        if location_id:
            detail = f"Локация с id {location_id} не найдена"
        if name:
            detail = f"Локация с именем {name} не найдена"
        super().__init__(detail=detail)


class LocationAlreadyExistsException(BaseDatabaseException):
    def __init__(self, name: str) -> None:
        detail = f"Локация с именем {name} уже существует"
        super().__init__(detail=detail)


class DatabaseOperationException(BaseDatabaseException):
    def __init__(self, operation: str, detail: str = None) -> None:
        message = f"Ошибка при выполнении операции '{operation}'"
        if detail:
            message += f": {detail}"
        super().__init__(detail=message)
