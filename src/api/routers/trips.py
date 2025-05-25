from datetime import datetime
from typing import Optional

import fastapi
from fastapi import APIRouter, HTTPException

from src.api.views.trip import TripPoint as AWTripPoint
from src.api.views.trip import Trip as AWTrip
from src.api.models.trip import Trip as AMTrip

from src.db.schemes.trip import Trip as DBTrip
from src.db.schemes.trip_point import TripPoint as DBTripPoint

from src.db.session import session

router = APIRouter(prefix="/trips", tags=["Trips"])

@router.get("/{trip_id}")
async def trip(trip_id: int) -> AWTrip:
    try:
        s = session()
    except:
        raise fastapi.HTTPException(500)

    tmp = s.get(DBTrip, trip_id)

    if not tmp:
        raise HTTPException(status_code=404, detail="Trip not found")

    points = s.query(DBTripPoint).filter(DBTripPoint.TripID == trip_id).all()

    if not len(points):
        raise HTTPException(status_code=405, detail="Trip points missing")

    points: list[AWTripPoint] = []

    for point in points:
        points.append(AWTripPoint(
            facility_id=point.FacilityID,
            is_first=point.IsFirst
        ))

    return AWTrip(
        trip_id=trip_id,
        employee_id=tmp.EmployeeID,
        from_time=tmp.FromTime,
        to_time=tmp.ToTime,
        points=points,
    )

@router.put("/update/{trip_id}")
async def start_update(trip_id: int, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None):
    s = session()
    t = s.get(DBTrip, trip_id)

    if not t:
        raise HTTPException(status_code=404, detail="Trip not found")

    if start_time:
        t.FromTime = start_time

    if end_time:
        t.ToTime = end_time

    s.commit()

@router.post("/new")
async def new_trip(body : AMTrip) -> None:
    s = session()

    print(body)

    tmp = DBTrip(
        EmployeeID=body.employee_id,
        FromTime=body.from_time,
        ToTime=body.to_time
    )

    s.add(tmp)
    s.commit()
    s.refresh(tmp)

    for i in body.points:
        s.add(DBTripPoint(
            TripID=tmp.TripID,
            FacilityID=i.facility_id,
            IsFirst=i.is_first
        ))

    s.commit()


@router.get("/actives")
def actives_trips() -> list[AWTrip]:
    try:
        s = session()
    except:
        raise fastapi.HTTPException(500)


    trips = []

    for tmp in s.query(DBTrip).filter(DBTrip.ToTime is None).all():
        if not tmp:
            raise HTTPException(status_code=404, detail="Trip not found")

        points = s.query(DBTripPoint).filter(DBTripPoint.TripID == tmp.TripID).all()

        if not len(points):
            raise HTTPException(status_code=405, detail="Trip points missing")

        points: list[AWTripPoint] = []

        for point in points:
            points.append(AWTripPoint(
                facility_id=point.FacilityID,
                is_first=point.IsFirst
            ))

        trips.append(AWTrip(
            trip_id=tmp.TripID,
            employee_id=tmp.EmployeeID,
            from_time=tmp.FromTime,
            to_time=tmp.ToTime,
            points=points,
        ))

    return trips