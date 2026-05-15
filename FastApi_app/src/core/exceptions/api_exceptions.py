from fastapi import HTTPException, status


class NotFoundException(HTTPException):
    def __init__(self, detail: str = "Ресурс не найден") -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )


class ConflictException(HTTPException):
    def __init__(self, detail: str = "Запись уже существует") -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
        )


class ForbiddenException(HTTPException):
    def __init__(self, detail: str = "Нет прав для выполнения операции") -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )


class CredentialsException(HTTPException):
    def __init__(self, detail: str = "Неверные учетные данные") -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class UserAlreadyExistsException(ConflictException):
    def __init__(self, login: str):
        super().__init__(detail=f"Пользователь с логином '{login}' уже существует")


class UserNotFoundException(NotFoundException):
    def __init__(self, user_id: int = None, login: str = None):
        if user_id:
            detail = f"Пользователь с id '{user_id}' не найден"
        elif login:
            detail = f"Пользователь с логином '{login}' не найден"
        else:
            detail = "Пользователь не найден"
        super().__init__(detail=detail)


class UserDeletedSuccessfullyException(HTTPException):
    def __init__(self, user_id: int, login: str = None):
        message = f"Пользователь с id '{user_id}' успешно удален"
        if login:
            message = f"Пользователь '{login}' успешно удален"
        super().__init__(
            status_code=status.HTTP_200_OK,
            detail={
                "status": "success",
                "message": message,
                "user_id": user_id
            }
        )


class ProfileUpdatedSuccessfullyException(HTTPException):
    def __init__(self, user_id: int, login: str):
        super().__init__(
            status_code=status.HTTP_200_OK,
            detail={
                "status": "success",
                "message": f"Профиль пользователя '{login}' успешно обновлен",
                "user_id": user_id,
                "login": login
            }
        )


class InvalidCredentialsException(CredentialsException):
    def __init__(self):
        super().__init__(detail="Неверный логин или пароль")


class InvalidTokenException(CredentialsException):
    def __init__(self):
        super().__init__(detail="Недействительный токен")


class AdminRequiredException(ForbiddenException):
    def __init__(self):
        super().__init__(detail="Требуются права администратора")