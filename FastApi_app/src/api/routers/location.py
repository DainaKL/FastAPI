from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.depends import get_location_use_cases
from src.core.exceptions.domain_exceptions import (
    LocationAlreadyExistsException, LocationNotFoundByNameException,
    LocationNotFoundException)
from src.domain.location.use_cases.location_use_cases import LocationUseCases
from src.schemas.location import Location, LocationCreate, LocationUpdate

router = APIRouter(prefix="/locations", tags=["Locations"])


@router.get("/", response_model=List[Location])
async def get_locations(
    skip: int = 0,
    limit: int = 100,
    use_cases: LocationUseCases = Depends(get_location_use_cases),
):
    return await use_cases.get_all(skip=skip, limit=limit)


@router.get("/published", response_model=List[Location])
async def get_published_locations(
    skip: int = 0,
    limit: int = 100,
    use_cases: LocationUseCases = Depends(get_location_use_cases),
):
    return await use_cases.get_published(skip=skip, limit=limit)


@router.get("/{location_id}", response_model=Location)
async def get_location(
    location_id: int,
    use_cases: LocationUseCases = Depends(get_location_use_cases),
):
    try:
        return await use_cases.get_by_id(location_id)
    except LocationNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.get_detail())


@router.get("/name/{name}", response_model=Location)
async def get_location_by_name(
    name: str,
    use_cases: LocationUseCases = Depends(get_location_use_cases),
):
    try:
        return await use_cases.get_by_name(name)
    except LocationNotFoundByNameException as e:
        raise HTTPException(status_code=404, detail=e.get_detail())


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Location)
async def create_location(
    location_data: LocationCreate,
    use_cases: LocationUseCases = Depends(get_location_use_cases),
):
    try:
        return await use_cases.create(location_data)
    except LocationAlreadyExistsException as e:
        raise HTTPException(status_code=409, detail=e.get_detail())


@router.put("/{location_id}", response_model=Location)
async def update_location(
    location_id: int,
    location_data: LocationUpdate,
    use_cases: LocationUseCases = Depends(get_location_use_cases),
):
    try:
        return await use_cases.update(location_id, location_data)
    except LocationNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.get_detail())


@router.delete("/{location_id}")
async def delete_location(
    location_id: int,
    use_cases: LocationUseCases = Depends(get_location_use_cases),
):
    try:
        await use_cases.delete(location_id)
        return {"message": "Location deleted"}
    except LocationNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.get_detail())
