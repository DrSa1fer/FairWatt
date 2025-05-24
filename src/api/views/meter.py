from pydantic import BaseModel
from typing import Literal, Optional

class MeterDetail(BaseModel):
    resident_count      : Optional[int]
    room_count          : Optional[int]
    square              : Optional[float]
    facility_type_name  : Optional[str]

class Geodata(BaseModel):
    latitude : float
    longitude : float

class Meter(BaseModel):
    meter_id: int
    facility_id: int
    name:  Optional[str]
    rating:  Optional[int]
    address:  Optional[str]

    meter_details : MeterDetail

    geodata:  Optional[Geodata]
    consumption: Optional[list[float]]
    is_daily: bool
    verified_status : Optional[str]
    is_first:  Optional[bool]
