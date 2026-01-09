from pydantic import BaseModel, Field


class SpyCatBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    years_of_experience: int = Field(..., ge=0)
    breed: str = Field(..., min_length=1, max_length=100)


class SpyCatCreate(SpyCatBase):
    salary: float = Field(..., gt=0)


class SpyCatUpdate(BaseModel):
    salary: float = Field(..., gt=0)


class SpyCatRead(SpyCatBase):
    id: int
    salary: float

    class Config:
        from_attributes = True
