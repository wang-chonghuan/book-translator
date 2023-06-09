from typing import Optional
from pydantic import Field
from models.base import MongoBaseModel

class CarBase(MongoBaseModel):
    brand: str = Field(..., min_length=1)
    make: str = Field(..., min_length=1)
    year: int = Field(..., gt=1975, lt=2023)
    price: int = Field(...)
    km: int = Field(...)
    cm3: int = Field(...)

class CarDB(CarBase):
    owner: str = Field(...)

class CarUpdate(MongoBaseModel):
    price: Optional[int] = None
