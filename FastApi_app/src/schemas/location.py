from datetime import datetime
from pydantic import field_validator

from src.schemas.base import BaseSchema


class LocationBase(BaseSchema):
    name: str
    is_published: bool = True

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if len(v) < 2:
            raise ValueError("Название локации должно содержать минимум 2 символа")
        if len(v) > 256:
            raise ValueError(
                "Название локации должно содержать максимум 256 символов"
            )
        return v


class LocationCreate(LocationBase):
    pass


class LocationUpdate(BaseSchema):
    name: str | None = None
    is_published: bool | None = None


class Location(LocationBase):
    id: int
    created_at: datetime
