from fastapi import HTTPException, status
from typing import List
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.location_repository import (
    LocationRepository,
)
from src.infrastructure.sqlite.models.location import Location as LocationModel
from src.schemas.location import LocationCreate, LocationUpdate, Location


class LocationUseCases:
    def __init__(self):
        self._database = database

    async def create(self, data: LocationCreate) -> Location:
        with self._database.session() as session:
            repo = LocationRepository(session)
            existing = repo.get_by_name(data.name)
            if existing:
                raise HTTPException(
                    status_code=400, detail="Location with this name already exists"
                )
            location = LocationModel(**data.model_dump())
            created = repo.create(location)
            return Location.model_validate(created, from_attributes=True)

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Location]:
        with self._database.session() as session:
            repo = LocationRepository(session)
            locations = repo.get_all(skip=skip, limit=limit)
            return [Location.model_validate(l, from_attributes=True) for l in locations]

    async def get_published(self, skip: int = 0, limit: int = 100) -> List[Location]:
        with self._database.session() as session:
            repo = LocationRepository(session)
            locations = repo.get_published(skip=skip, limit=limit)
            return [Location.model_validate(l, from_attributes=True) for l in locations]

    async def get_by_id(self, location_id: int) -> Location:
        with self._database.session() as session:
            repo = LocationRepository(session)
            location = repo.get_by_id(location_id)
            if not location:
                raise HTTPException(status_code=404, detail="Location not found")
            return Location.model_validate(location, from_attributes=True)

    async def get_by_name(self, name: str) -> Location:
        with self._database.session() as session:
            repo = LocationRepository(session)
            location = repo.get_by_name(name)
            if not location:
                raise HTTPException(status_code=404, detail="Location not found")
            return Location.model_validate(location, from_attributes=True)

    async def update(self, location_id: int, data: LocationUpdate) -> Location:
        with self._database.session() as session:
            repo = LocationRepository(session)
            location = repo.get_by_id(location_id)
            if not location:
                raise HTTPException(status_code=404, detail="Location not found")
            update_dict = {k: v for k, v in data.model_dump().items() if v is not None}
            updated = repo.update(location, update_dict)
            return Location.model_validate(updated, from_attributes=True)

    async def delete(self, location_id: int) -> None:
        with self._database.session() as session:
            repo = LocationRepository(session)
            location = repo.get_by_id(location_id)
            if not location:
                raise HTTPException(status_code=404, detail="Location not found")
            repo.delete(location)
