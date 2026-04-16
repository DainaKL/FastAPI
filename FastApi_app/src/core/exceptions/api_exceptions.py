from src.core.exceptions.base_exceptions import BaseAPIException


class NotFoundAPIException(BaseAPIException):
    def __init__(self, detail: str = "Ресурс не найден") -> None:
        super().__init__(detail=detail, status_code=404)


class ConflictAPIException(BaseAPIException):
    def __init__(self, detail: str = "Конфликт данных") -> None:
        super().__init__(detail=detail, status_code=409)


class BadRequestAPIException(BaseAPIException):
    def __init__(self, detail: str = "Неверный запрос") -> None:
        super().__init__(detail=detail, status_code=400)


class UnauthorizedAPIException(BaseAPIException):
    def __init__(self, detail: str = "Не авторизован") -> None:
        super().__init__(detail=detail, status_code=401)


class ForbiddenAPIException(BaseAPIException):
    def __init__(self, detail: str = "Доступ запрещен") -> None:
        super().__init__(detail=detail, status_code=403)


class InternalServerErrorAPIException(BaseAPIException):
    def __init__(self, detail: str = "Внутренняя ошибка сервера") -> None:
        super().__init__(detail=detail, status_code=500)


class ValidationErrorAPIException(BaseAPIException):
    def __init__(self, detail: str = "Ошибка валидации") -> None:
        super().__init__(detail=detail, status_code=422)
