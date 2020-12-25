from typing import List, Optional
from pydantic import BaseModel, Field


class CarBase(BaseModel):
    make: str
    model: str

    class Config:
        orm_mode = True


class Car(CarBase):
    id: int
    make: str
    model: str
    average_rate: float
    rates_sum: int
    rates_number: int

    class Config:
        orm_mode = True


class Rate(BaseModel):
    make: str
    model: str
    score: int = Field(gt=0, lt=6, description="Score must be between 1 and 5")

    class Config:
        orm_mode = True
