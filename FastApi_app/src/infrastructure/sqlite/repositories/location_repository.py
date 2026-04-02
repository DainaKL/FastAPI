from sqlalchemy import select
from sqlalchemy.orm import Session

from src.infrastructure.sqlite.models import Location
from src.infrastructure.sqlite.repositories.base import BaseRepository


class LocationRepository(BaseRepository[Location]):
    def __init__(self, session: Session):
        super().__init__(session, Location)

    def get_by_name(self, name: str) -> Location | None:
        stmt = select(Location).where(Location.name == name)
        return self.session.execute(stmt).scalar_one_or_none()

    def get_published(self, skip: int = 0, limit: int = 100) -> list[Location]:
        stmt = (
            select(Location)
            .where(Location.is_published)
            .offset(skip)
            .limit(limit)
        )
        return self.session.execute(stmt).scalars().all()
