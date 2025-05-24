from datetime import datetime
from fastapi import APIRouter, HTTPException

from src.api.models.trip import Trip as AMTrip
from src.api.views.trip import Trip as AWTrip, TripPoint as AWTripPoint
from src.db.schemes.trip import Trip as DBTrip
from src.db.schemes.trip_point import TripPoint as DBTripPoint

from src.db.session import session

router = APIRouter(prefix="/trips", tags=["trips"])

@router.get("/getTrip")
async def trip(trip_id: int) -> AWTrip:
    s = session()
    t = s.get(DBTrip, trip_id)

    if not t:
        raise HTTPException(status_code=404, detail="Trip not found")

    db_points = s.query(DBTripPoint).filter(DBTripPoint.TripID == trip_id).all()

    if not db_points:
        raise HTTPException(status_code=404, detail="Trip not found")

    points: list[AWTripPoint] = []

    for point in db_points:
        points.append(AWTripPoint(
            facility_id=point.FacilityID,
            is_first=point.IsFirst
        ))

    return AWTrip(
        trip_id=trip_id,
        employee_id=t.EmployeeID,
        from_time=t.FromTime,
        to_time=t.ToTime,
        points=points,
    )

@router.put("/updateStartTime")
async def start_update(trip_id: int, start_time: datetime):
    s = session()
    t = s.get(DBTrip, trip_id)

    if not t:
        raise HTTPException(status_code=404, detail="Trip not found")

    t.StartTime = start_time
    s.commit()

@router.put("/updateEndTime")
async def end_update(trip_id: int, end_time: datetime):
    s = session()
    t = s.get(DBTrip, trip_id)

    if not t:
        raise HTTPException(status_code=404, detail="Trip not found")

    t.ToTime = end_time
    s.commit()


@router.post("/create")
async def new_trip(body : AMTrip) -> None:
    s = session()

    s.add(DBTrip(
        EmployeeID=body.employee_id,
        FromTime=body.from_time,
        ToTime=body.to_time
    ))

    for i in body.points:
        s.add(DBTripPoint(
            TripID=body.trip_id,
            FacilityID=i.facility_id,
            IsFirst=i.is_first
        ))

    s.commit()