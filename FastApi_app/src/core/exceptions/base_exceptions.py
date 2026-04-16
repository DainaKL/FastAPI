class BaseDomainException(Exception):
    def __init__(self, detail: str) -> None:
        self._detail = detail

    def get_detail(self) -> str:
        return self._detail


class BaseDatabaseException(Exception):
    def __init__(self, detail: str | None = None) -> None:
        self._detail = detail

    def get_detail(self) -> str | None:
        return self._detail


class BaseAPIException(Exception):
    def __init__(self, detail: str, status_code: int) -> None:
        self._detail = detail
        self._status_code = status_code

    def get_detail(self) -> str:
        return self._detail

    def get_status_code(self) -> int:
        return self._status_code
