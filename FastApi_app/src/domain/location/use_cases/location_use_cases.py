from typing import List

from fastapi import HTTPException

from src.core.exceptions.database_exceptions import (
    DatabaseOperationException, LocationAlreadyExistsException,
    LocationNotFoundException)
from src.core.exceptions.domain_exceptions import \
    LocationAlreadyExistsException as DomainLocationAlreadyExistsException
from src.core.exceptions.domain_exceptions import \
    LocationNotFoundByNameException
from src.core.exceptions.domain_exceptions import \
    LocationNotFoundException as DomainLocationNotFoundException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.location_repository import \
    LocationRepository
from src.schemas.location import Location, LocationCreate, LocationUpdate


class LocationUseCases:
    def __init__(self):
        self._database = database

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Location]:
        with self._database.session() as session:
            repo = LocationRepository(session)
            try:
                locations = repo.get_all(skip=skip, limit=limit)
                return [
                    Location.model_validate(l, from_attributes=True) for l in locations
                ]
            except DatabaseOperationException as e:
                raise HTTPException(status_code=500, detail=e.get_detail())

    async def get_published(self, skip: int = 0, limit: int = 100) -> List[Location]:
        with self._database.session() as session:
            repo = LocationRepository(session)
            try:
                locations = repo.get_published(skip=skip, limit=limit)
                return [
                    Location.model_validate(l, from_attributes=True) for l in locations
                ]
            except DatabaseOperationException as e:
                raise HTTPException(status_code=500, detail=e.get_detail())

    async def get_by_id(self, location_id: int) -> Location:
        with self._database.session() as session:
            repo = LocationRepository(session)
            try:
                location = repo.get_by_id(location_id)
                return Location.model_validate(location, from_attributes=True)
            except LocationNotFoundException:
                raise DomainLocationNotFoundException(location_id=location_id)
            except DatabaseOperationException as e:
                raise HTTPException(status_code=500, detail=e.get_detail())

    async def get_by_name(self, name: str) -> Location:
        with self._database.session() as session:
            repo = LocationRepository(session)
            try:
                location = repo.get_by_name(name)
                if not location:
                    raise LocationNotFoundByNameException(name=name)
                return Location.model_validate(location, from_attributes=True)
            except LocationNotFoundByNameException:
                raise
            except DatabaseOperationException as e:
                raise HTTPException(status_code=500, detail=e.get_detail())

    async def create(self, data: LocationCreate) -> Location:
        with self._database.session() as session:
            repo = LocationRepository(session)
            try:
                location_dict = data.model_dump()
                location = repo.create(**location_dict)
                return Location.model_validate(location, from_attributes=True)
            except LocationAlreadyExistsException:
                raise DomainLocationAlreadyExistsException(name=data.name)
            except DatabaseOperationException as e:
                raise HTTPException(status_code=500, detail=e.get_detail())

    async def update(self, location_id: int, data: LocationUpdate) -> Location:
        with self._database.session() as session:
            repo = LocationRepository(session)
            try:
                update_dict = {
                    k: v for k, v in data.model_dump().items() if v is not None
                }
                location = repo.update(location_id, **update_dict)
                return Location.model_validate(location, from_attributes=True)
            except LocationNotFoundException:
                raise DomainLocationNotFoundException(location_id=location_id)
            except DatabaseOperationException as e:
                raise HTTPException(status_code=500, detail=e.get_detail())

    async def delete(self, location_id: int) -> None:
        with self._database.session() as session:
            repo = LocationRepository(session)
            try:
                repo.delete(location_id)
            except LocationNotFoundException:
                raise DomainLocationNotFoundException(location_id=location_id)
            except DatabaseOperationException as e:
                raise HTTPException(status_code=500, detail=e.get_detail())
