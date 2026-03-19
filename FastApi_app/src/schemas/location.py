from datetime import datetime

from pydantic import Field

from src.schemas.base import BaseSchema


class LocationBase(BaseSchema):
    name: str 
    is_published: bool = True


class LocationCreate(LocationBase):
    pass


class LocationUpdate(BaseSchema):
    name: str | None = None
    is_published: bool | None = None


class Location(LocationBase):
    id: int
    created_at: datetime
