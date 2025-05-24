from typing import List
from fastapi import APIRouter, HTTPException

from src.api.models.meter import Meter as MeterModel, MeterDetails
from src.api.models.trip import Trip as AMTrip
from src.api.views.trip import Trip as AWTrip
from src.db.schemes.employee import Employee
from src.db.schemes.trip import Trip as DBTrip
from src.db.schemes.trip_point import TripPoint

from src.db.session import session

router = APIRouter()

@router.get("/trip/{trip_id}")
async def trip(trip_id: int) -> AWTrip:
    s = session()
    t = s.get(DBTrip, trip_id)

    if t






@router.post("/trip/new")
async def new_trip(body : AMTrip) -> None:
    s = session()

    s.add(DBTrip(
        EmployeeID=body.employee_id,
        FromTime=body.from_time,
        ToTime=body.to_time
    ))

    for i in body.points:
        s.add(TripPoint(
            TripID=body.trip_id,
            FacilityID=i.facility_id,
            IsFirst=i.is_first
        ))

    s.commit()