from sqlalchemy.orm import Session

from src.infrastructure.sqlite.models import Location
from src.infrastructure.sqlite.repositories.base import BaseRepository


class LocationRepository(BaseRepository[Location]):
    def __init__(self, session: Session):
        super().__init__(session, Location)
