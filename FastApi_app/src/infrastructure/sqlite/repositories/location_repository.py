from typing import List, Optional
from sqlalchemy.orm import Session
from src.infrastructure.sqlite.models.location import Location as LocationModel


class LocationRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, location: LocationModel) -> LocationModel:
        self.session.add(location)
        self.session.flush()
        return location

    def get_all(self, skip: int = 0, limit: int = 100) -> List[LocationModel]:
        return self.session.query(LocationModel).offset(skip).limit(limit).all()

    def get_published(self, skip: int = 0, limit: int = 100) -> List[LocationModel]:
        return (
            self.session.query(LocationModel)
            .filter(LocationModel.is_published == True)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_id(self, location_id: int) -> Optional[LocationModel]:
        return (
            self.session.query(LocationModel)
            .filter(LocationModel.id == location_id)
            .first()
        )

    def get_by_name(self, name: str) -> Optional[LocationModel]:
        return (
            self.session.query(LocationModel).filter(LocationModel.name == name).first()
        )

    def update(self, location: LocationModel, data: dict) -> LocationModel:
        for key, value in data.items():
            setattr(location, key, value)
        self.session.flush()
        return location

    def delete(self, location: LocationModel) -> None:
        self.session.delete(location)
        self.session.flush()
