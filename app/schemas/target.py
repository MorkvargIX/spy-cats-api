from typing import Optional

from pydantic import BaseModel, Field


class TargetBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    country: str = Field(..., min_length=1, max_length=100)


class TargetCreate(TargetBase):
    notes: Optional[str] = None


class TargetUpdate(BaseModel):
    notes: Optional[str] = None
    is_completed: Optional[bool] = None


class TargetRead(TargetBase):
    id: int
    notes: Optional[str]
    is_completed: bool

    model_config = {"from_attributes": True}


class TargetOut(BaseModel):
    id: int
    name: str
    country: str
    notes: str | None
    is_completed: bool

    model_config = {"from_attributes": True}
