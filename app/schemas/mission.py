from typing import List, Optional

from pydantic import BaseModel, field_validator

from app.schemas.target import TargetCreate, TargetRead


class MissionCreate(BaseModel):
    targets: list[TargetCreate]

    @field_validator("targets")
    @classmethod
    def validate_targets_count(cls, v):
        if not (1 <= len(v) <= 3):
            raise ValueError("Mission must have between 1 and 3 targets")
        return v


class MissionAssign(BaseModel):
    cat_id: int


class MissionRead(BaseModel):
    id: int
    cat_id: Optional[int]
    is_completed: bool
    targets: List[TargetRead]

    model_config = {"from_attributes": True}
