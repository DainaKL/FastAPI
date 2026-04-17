from fastapi import HTTPException, status


class CredentialsException(HTTPException):
    def __init__(self, detail: str = "Could not validate credentials") -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class NotFoundException(HTTPException):
    def __init__(self, detail: str = "Ресурс не найден") -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )


class ConflictException(HTTPException):
    def __init__(self, detail: str = "Конфликт данных") -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
        )


class BadRequestException(HTTPException):
    def __init__(self, detail: str = "Неверный запрос") -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )


class ForbiddenException(HTTPException):
    def __init__(self, detail: str = "Доступ запрещен") -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )


class InternalServerErrorException(HTTPException):
    def __init__(self, detail: str = "Внутренняя ошибка сервера") -> None:
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
        )


class ValidationErrorException(HTTPException):
    def __init__(self, detail: str = "Ошибка валидации") -> None:
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
        )
