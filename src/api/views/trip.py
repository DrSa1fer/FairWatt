from datetime import datetime
from pydantic import BaseModel

class TripPoint(BaseModel):
    facility_id: int
    is_first: bool

class Trip(BaseModel):
    trip_id: int
    employee_id: int
    from_time: datetime | None
    to_time: datetime | None
    points : list[TripPoint]

