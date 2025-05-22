from pydantic import BaseModel
from typing import Literal

FACILITY = Literal["house", "flat"]

class MeterDetails(BaseModel):
    square: int
    hasElectricHeating: bool
    hasElectricStove: bool
    facilityName: FACILITY

class Meter(BaseModel):
    id: int
    name: str
    rating: int
    address: str
    lastConsumption: int
    tariffName: str
    tariffPrice: float
    region: str
    meterDetails: MeterDetails

