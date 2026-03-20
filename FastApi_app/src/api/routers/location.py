from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from src.api.depends import get_location_repository
from src.schemas.location import Location, LocationCreate, LocationUpdate
from src.infrastructure.sqlite.repositories.location_repository import LocationRepository

router = APIRouter(prefix="/locations", tags=["Locations"])


@router.get("/", response_model=List[Location])
async def get_locations(
    skip: int = 0,
    limit: int = 100,
    repo: LocationRepository = Depends(get_location_repository)
):
    """Получение списка всех локаций"""
    try:
        locations = repo.get_all(skip=skip, limit=limit)
        return locations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/published", response_model=List[Location])
async def get_published_locations(
    skip: int = 0,
    limit: int = 100,
    repo: LocationRepository = Depends(get_location_repository)
):
    """Получение только опубликованных локаций"""
    try:
        locations = repo.get_published(skip=skip, limit=limit)
        return locations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{location_id}", response_model=Location)
async def get_location(
    location_id: int,
    repo: LocationRepository = Depends(get_location_repository)
):
    """Получение локации по ID"""
    location = repo.get_by_id(location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return location


@router.get("/name/{name}", response_model=Location)
async def get_location_by_name(
    name: str,
    repo: LocationRepository = Depends(get_location_repository)
):
    """Получение локации по названию"""
    location = repo.get_by_name(name)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return location


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Location)
async def create_location(
    location_data: LocationCreate,
    repo: LocationRepository = Depends(get_location_repository)
):
    """Создание новой локации"""
    try:
        # Проверка на существующую локацию
        existing = repo.get_by_name(location_data.name)
        if existing:
            raise HTTPException(status_code=400, detail="Location with this name already exists")
        
        location_dict = location_data.model_dump()
        new_location = repo.create(**location_dict)
        return new_location
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{location_id}", response_model=Location)
async def update_location(
    location_id: int,
    location_data: LocationUpdate,
    repo: LocationRepository = Depends(get_location_repository)
):
    """Обновление локации"""
    try:
        update_dict = {k: v for k, v in location_data.model_dump().items() if v is not None}
        updated = repo.update(location_id, **update_dict)
        if not updated:
            raise HTTPException(status_code=404, detail="Location not found")
        return updated
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{location_id}")
async def delete_location(
    location_id: int,
    repo: LocationRepository = Depends(get_location_repository)
):
    """Удаление локации"""
    deleted = repo.delete(location_id)
    try:
        if not deleted:
            raise HTTPException(status_code=404, detail="Location not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    