from src.core.exceptions.base_exceptions import BaseDomainException


class UserNotFoundByLoginException(BaseDomainException):
    _exception_text_template = "Пользователь с логином {login} не найден"

    def __init__(self, login: str) -> None:
        detail = self._exception_text_template.format(login=login)
        super().__init__(detail=detail)


class UserLoginIsNotUniqueException(BaseDomainException):
    _exception_text_template = "Пользователь с логином {login} уже существует"

    def __init__(self, login: str) -> None:
        detail = self._exception_text_template.format(login=login)
        super().__init__(detail=detail)


class PostNotFoundException(BaseDomainException):
    _exception_text_template = "Пост с id {post_id} не найден"

    def __init__(self, post_id: int) -> None:
        detail = self._exception_text_template.format(post_id=post_id)
        super().__init__(detail=detail)


class CommentNotFoundException(BaseDomainException):
    _exception_text_template = "Комментарий с id {comment_id} не найден"

    def __init__(self, comment_id: int) -> None:
        detail = self._exception_text_template.format(comment_id=comment_id)
        super().__init__(detail=detail)


class CategoryNotFoundException(BaseDomainException):
    _exception_text_template = "Категория с id {category_id} не найдена"

    def __init__(self, category_id: int) -> None:
        detail = self._exception_text_template.format(category_id=category_id)
        super().__init__(detail=detail)


class CategoryNotFoundBySlugException(BaseDomainException):
    _exception_text_template = "Категория {slug} не найдена"

    def __init__(self, slug: str) -> None:
        detail = self._exception_text_template.format(slug=slug)
        super().__init__(detail=detail)


class LocationNotFoundException(BaseDomainException):
    _exception_text_template = "Локация с id {location_id} не найдена"

    def __init__(self, location_id: int) -> None:
        detail = self._exception_text_template.format(location_id=location_id)
        super().__init__(detail=detail)


class LocationNotFoundByNameException(BaseDomainException):
    _exception_text_template = "Локация {name} не найдена"

    def __init__(self, name: str) -> None:
        detail = self._exception_text_template.format(name=name)
        super().__init__(detail=detail)


class LocationAlreadyExistsException(BaseDomainException):
    _exception_text_template = "Локация {name} уже существует"

    def __init__(self, name: str) -> None:
        detail = self._exception_text_template.format(name=name)
        super().__init__(detail=detail)
