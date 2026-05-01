from src.core.exceptions.base_exceptions import BaseDomainException


class InvalidPasswordException(BaseDomainException):
    _exception_text_template = "Неверный пароль"

    def __init__(self) -> None:
        super().__init__(detail=self._exception_text_template)
