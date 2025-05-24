from pydantic import BaseModel
from typing import Literal, Optional

class MeterDetail(BaseModel):
    resident_count      : Optional[int]
    room_count          : Optional[int]
    square              : Optional[float]
    facility_type_name  : Optional[str]
    tariff_price        : Optional[float]
    tariff_type_name    : Optional[str]

class Geodata(BaseModel):
    latitude : float
    longitude : float


class Client(BaseModel):
    client_id : int
    name : str
    phone : str
    email : Optional[str]

class Meter(BaseModel):
    meter_id        : int
    facility_id     : int
    rating          : Optional[float]
    address         : Optional[str]

    is_iot          : bool
    consumption     : Optional[list[float]]

    client          : Client
    meter_details   : MeterDetail
    geodata         : Optional[Geodata]
    verified_status : Optional[str]
    is_first        : Optional[bool]
