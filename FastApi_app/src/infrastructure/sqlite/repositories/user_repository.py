from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import select

from src.infrastructure.sqlite.models import User
from src.infrastructure.sqlite.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: Session):
        super().__init__(session, User)
    
    def get_by_login(self, login: str) -> Optional[User]:
        stmt = select(User).where(User.login == login)
        return self.session.execute(stmt).scalar_one_or_none()
