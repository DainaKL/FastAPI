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
            detail={"status": "success", "message": message, "user_id": user_id},
        )


class ProfileUpdatedSuccessfullyException(HTTPException):
    def __init__(self, user_id: int, login: str):
        super().__init__(
            status_code=status.HTTP_200_OK,
            detail={
                "status": "success",
                "message": f"Профиль пользователя '{login}' успешно обновлен",
                "user_id": user_id,
                "login": login,
            },
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


class PostNotFoundException(NotFoundException):
    def __init__(self, post_id: int):
        super().__init__(detail=f"Пост с id '{post_id}' не найден")


class PostDeletedSuccessfullyException(HTTPException):
    def __init__(self, post_id: int):
        super().__init__(
            status_code=status.HTTP_200_OK,
            detail={
                "status": "success",
                "message": f"Пост с id '{post_id}' успешно удален",
                "post_id": post_id,
            },
        )


class PostUpdatedSuccessfullyException(HTTPException):
    def __init__(self, post_id: int):
        super().__init__(
            status_code=status.HTTP_200_OK,
            detail={
                "status": "success",
                "message": f"Пост с id '{post_id}' успешно обновлен",
                "post_id": post_id,
            },
        )


class PostCreatedSuccessfullyException(HTTPException):
    def __init__(self, post_id: int):
        super().__init__(
            status_code=status.HTTP_201_CREATED,
            detail={
                "status": "success",
                "message": f"Пост с id '{post_id}' успешно создан",
                "post_id": post_id,
            },
        )


class CommentNotFoundException(NotFoundException):
    def __init__(self, comment_id: int):
        super().__init__(detail=f"Комментарий с id '{comment_id}' не найден")


class CommentDeletedSuccessfullyException(HTTPException):
    def __init__(self, comment_id: int):
        super().__init__(
            status_code=status.HTTP_200_OK,
            detail={
                "status": "success",
                "message": f"Комментарий с id '{comment_id}' успешно удален",
                "comment_id": comment_id,
            },
        )


class CommentUpdatedSuccessfullyException(HTTPException):
    def __init__(self, comment_id: int):
        super().__init__(
            status_code=status.HTTP_200_OK,
            detail={
                "status": "success",
                "message": f"Комментарий с id '{comment_id}' успешно обновлен",
                "comment_id": comment_id,
            },
        )


class CommentCreatedSuccessfullyException(HTTPException):
    def __init__(self, comment_id: int):
        super().__init__(
            status_code=status.HTTP_201_CREATED,
            detail={
                "status": "success",
                "message": f"Комментарий с id '{comment_id}' успешно создан",
                "comment_id": comment_id,
            },
        )


class CategoryNotFoundException(NotFoundException):
    def __init__(self, category_id: int = None, slug: str = None):
        if category_id:
            detail = f"Категория с id '{category_id}' не найдена"
        elif slug:
            detail = f"Категория со slug '{slug}' не найдена"
        else:
            detail = "Категория не найдена"
        super().__init__(detail=detail)


class CategorySlugAlreadyExistsException(ConflictException):
    def __init__(self, slug: str):
        super().__init__(detail=f"Категория со slug '{slug}' уже существует")


class CategoryDeletedSuccessfullyException(HTTPException):
    def __init__(self, category_id: int):
        super().__init__(
            status_code=status.HTTP_200_OK,
            detail={
                "status": "success",
                "message": f"Категория с id '{category_id}' успешно удалена",
                "category_id": category_id,
            },
        )


class CategoryUpdatedSuccessfullyException(HTTPException):
    def __init__(self, category_id: int):
        super().__init__(
            status_code=status.HTTP_200_OK,
            detail={
                "status": "success",
                "message": f"Категория с id '{category_id}' успешно обновлена",
                "category_id": category_id,
            },
        )


class CategoryCreatedSuccessfullyException(HTTPException):
    def __init__(self, category_id: int):
        super().__init__(
            status_code=status.HTTP_201_CREATED,
            detail={
                "status": "success",
                "message": f"Категория с id '{category_id}' успешно создана",
                "category_id": category_id,
            },
        )


class LocationNotFoundException(NotFoundException):
    def __init__(self, location_id: int = None, name: str = None):
        if location_id:
            detail = f"Локация с id '{location_id}' не найдена"
        elif name:
            detail = f"Локация с именем '{name}' не найдена"
        else:
            detail = "Локация не найдена"
        super().__init__(detail=detail)


class LocationAlreadyExistsException(ConflictException):
    def __init__(self, name: str):
        super().__init__(detail=f"Локация с именем '{name}' уже существует")


class LocationDeletedSuccessfullyException(HTTPException):
    def __init__(self, location_id: int):
        super().__init__(
            status_code=status.HTTP_200_OK,
            detail={
                "status": "success",
                "message": f"Локация с id '{location_id}' успешно удалена",
                "location_id": location_id,
            },
        )


class LocationUpdatedSuccessfullyException(HTTPException):
    def __init__(self, location_id: int):
        super().__init__(
            status_code=status.HTTP_200_OK,
            detail={
                "status": "success",
                "message": f"Локация с id '{location_id}' успешно обновлена",
                "location_id": location_id,
            },
        )


class LocationCreatedSuccessfullyException(HTTPException):
    def __init__(self, location_id: int):
        super().__init__(
            status_code=status.HTTP_201_CREATED,
            detail={
                "status": "success",
                "message": f"Локация с id '{location_id}' успешно создана",
                "location_id": location_id,
            },
        )


class CategoryForbiddenException(ForbiddenException):
    def __init__(self, action: str = "выполнения операции"):
        super().__init__(detail=f"Только администратор может {action} категории")


class CommentForbiddenException(ForbiddenException):
    def __init__(self, action: str = "редактировать/удалять"):
        super().__init__(detail=f"Вы можете {action} только свои комментарии")


class LocationForbiddenException(ForbiddenException):
    def __init__(self, action: str = "выполнения операции"):
        super().__init__(detail=f"Только администратор может {action} локации")


class PostForbiddenException(ForbiddenException):
    def __init__(self, action: str = "редактировать/удалять"):
        super().__init__(detail=f"Вы можете {action} только свои посты")


class PostAuthRequiredException(ForbiddenException):
    def __init__(self):
        super().__init__(detail="Необходимо авторизоваться")


class InvalidIDException(NotFoundException):
    def __init__(self, id_value: any):
        super().__init__(detail=f"Некорректный идентификатор '{id_value}'")
