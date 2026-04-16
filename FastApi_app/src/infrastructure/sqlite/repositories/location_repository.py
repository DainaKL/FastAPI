from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from src.core.exceptions.database_exceptions import (
    DatabaseOperationException, LocationAlreadyExistsException,
    LocationNotFoundException)
from src.infrastructure.sqlite.models.location import Location as LocationModel


class LocationRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self, skip: int = 0, limit: int = 100) -> List[LocationModel]:
        try:
            stmt = select(LocationModel).offset(skip).limit(limit)
            return list(self.session.execute(stmt).scalars().all())
        except SQLAlchemyError as e:
            raise DatabaseOperationException("get_all", str(e))

    def get_published(self, skip: int = 0, limit: int = 100) -> List[LocationModel]:
        try:
            stmt = (
                select(LocationModel)
                .where(LocationModel.is_published == True)
                .offset(skip)
                .limit(limit)
            )
            return list(self.session.execute(stmt).scalars().all())
        except SQLAlchemyError as e:
            raise DatabaseOperationException("get_published", str(e))

    def get_by_id(self, location_id: int) -> LocationModel:
        try:
            stmt = select(LocationModel).where(LocationModel.id == location_id)
            location = self.session.execute(stmt).scalar_one_or_none()
            if not location:
                raise LocationNotFoundException(location_id=location_id)
            return location
        except LocationNotFoundException:
            raise
        except SQLAlchemyError as e:
            raise DatabaseOperationException("get_by_id", str(e))

    def get_by_name(self, name: str) -> Optional[LocationModel]:
        try:
            stmt = select(LocationModel).where(LocationModel.name == name)
            return self.session.execute(stmt).scalar_one_or_none()
        except SQLAlchemyError as e:
            raise DatabaseOperationException("get_by_name", str(e))

    def create(self, **kwargs) -> LocationModel:
        try:
            existing = self.get_by_name(kwargs.get("name"))
            if existing:
                raise LocationAlreadyExistsException(name=kwargs.get("name"))
            location = LocationModel(**kwargs)
            self.session.add(location)
            self.session.flush()
            self.session.refresh(location)
            return location
        except LocationAlreadyExistsException:
            raise
        except IntegrityError as e:
            self.session.rollback()
            raise DatabaseOperationException("create", str(e))
        except SQLAlchemyError as e:
            self.session.rollback()
            raise DatabaseOperationException("create", str(e))

    def update(self, location_id: int, **kwargs) -> LocationModel:
        try:
            location = self.get_by_id(location_id)
            for key, value in kwargs.items():
                if hasattr(location, key):
                    setattr(location, key, value)
            self.session.flush()
            self.session.refresh(location)
            return location
        except LocationNotFoundException:
            raise
        except SQLAlchemyError as e:
            self.session.rollback()
            raise DatabaseOperationException("update", str(e))

    def delete(self, location_id: int) -> None:
        try:
            location = self.get_by_id(location_id)
            self.session.delete(location)
            self.session.flush()
        except LocationNotFoundException:
            raise
        except SQLAlchemyError as e:
            self.session.rollback()
            raise DatabaseOperationException("delete", str(e))
