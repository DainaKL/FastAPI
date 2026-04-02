from sqlalchemy import select
from sqlalchemy.orm import Session

from src.infrastructure.sqlite.models import User
from src.infrastructure.sqlite.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: Session):
        super().__init__(session, User)

    def get_by_login(self, login: str) -> User | None:
        if not login:
            return None
        stmt = select(User).where(User.login == login)
        return self.session.execute(stmt).scalar_one_or_none()

    def get_by_id(self, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        return self.session.execute(stmt).scalar_one_or_none()
