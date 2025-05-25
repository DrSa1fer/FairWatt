from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class TripPoint(BaseModel):
    facility_id: int
    is_first: bool

class Trip(BaseModel):
    employee_id: int
    from_time : Optional[datetime]
    to_time : Optional[datetime]
    points : list[TripPoint]

