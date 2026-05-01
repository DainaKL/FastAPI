from typing import Type
from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.infrastructure.sqlite.models.location import Location as LocationModel
from src.schemas.location import LocationCreate as LocationSchema
from src.core.exceptions.database_exceptions import (
    LocationAlreadyExistsException,
    DatabaseOperationException,
)


class LocationRepository:
    def __init__(self):
        self._model: Type[LocationModel] = LocationModel

    def get_by_id(self, session: Session, location_id: int):
        if location_id <= 0:
            return None
        query = select(self._model).where(self._model.id == location_id)
        return session.scalar(query)

    def get_by_name(self, session: Session, name: str):
        if not name:
            return None
        query = select(self._model).where(self._model.name == name)
        return session.scalar(query)

    def get_all(self, session: Session, skip: int = 0, limit: int = 100):
        query = select(self._model).offset(skip).limit(limit)
        return list(session.scalars(query).all())

    def get_published(self, session: Session, skip: int = 0, limit: int = 100):
        query = (
            select(self._model)
            .where(self._model.is_published == True)
            .offset(skip)
            .limit(limit)
        )
        return list(session.scalars(query).all())

    def create(self, session: Session, location: LocationSchema) -> LocationModel:
        existing = self.get_by_name(session, location.name)
        if existing:
            raise LocationAlreadyExistsException(name=location.name)
        try:
            query = (
                insert(self._model).values(location.model_dump()).returning(self._model)
            )
            return session.scalar(query)
        except IntegrityError as e:
            raise DatabaseOperationException("create", str(e))

    def update(self, session: Session, location_id: int, **kwargs):
        query = (
            update(self._model)
            .where(self._model.id == location_id)
            .values(**kwargs)
            .returning(self._model)
        )
        return session.scalar(query)

    def delete(self, session: Session, location_id: int):
        query = delete(self._model).where(self._model.id == location_id)
        result = session.execute(query)
        return result.rowcount > 0
