from datetime import datetime

from pydantic import BaseModel

class TripPoint(BaseModel):
    facility_id: int
    is_first: bool

class Trip(BaseModel):
    employee_id: int
    from_time : datetime
    to_time : datetime
    points : list[TripPoint]

