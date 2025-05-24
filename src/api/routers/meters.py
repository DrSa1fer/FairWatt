import random
from typing import List

import fastapi
from fastapi import APIRouter, HTTPException

from src.api.views.meter import Meter as AWMeter, MeterDetail, Geodata
from src.db.schemes.client import Client
from src.db.schemes.daily_consumption import DailyConsumption
from src.db.schemes.facility import Facility
from src.db.schemes.meter import Meter as DBMeter
from src.db.session import session

router = APIRouter()

def _new_meter(meter, consumption) -> AWMeter:
    client: Client = meter.Client
    facility: Facility = meter.Facility
    # tariff: Tariff = meter.Tariff

    return AWMeter(
        meter_id=meter.MeterID,
        facility_id=facility.FacilityID,
        name=f"{client.LastName} {client.FirstName} {client.FatherName}",
        rating=100 - (client.Rating * 100),
        address=facility.Address,
        meter_details=MeterDetail(
            resident_count=facility.Residents,
            room_count=facility.Rooms,
            square=facility.Square,
            facility_type_name=facility.FacilityKind
        ),
        geodata=Geodata(
            longitude=facility.Longitude,
            latitude=facility.Latitude
        ),
        consumption=consumption.Data
    )


@router.get("/meter/{meter_id}")
async def api_meter(meter_id: int) -> AWMeter | str:
    s = session()
    row = s.get(DBMeter, meter_id)

    if not row:
        raise HTTPException(status_code=404, detail="Meter not found")

    cons = s.query(DailyConsumption).filter(DailyConsumption.MeterID == meter_id).first()

    if not cons:
        raise HTTPException(status_code=400, detail="Meter not found")

    return _new_meter(s, cons.first())

@router.get("/meters")
async def api_meters(page: int = 0, per_page: int = 10) -> List[AWMeter]:
    if random.randint(0, 1000000) == 418:
        raise fastapi.HTTPException(418, "U win!")

    try:
        s = session()
    except RuntimeError as e:
        raise fastapi.HTTPException(500)

    if page < 1 or per_page < 1:
        raise fastapi.HTTPException(400)

    meters = []

    for row in (s.query(DBMeter).offset((page - 1) * per_page).limit(per_page)):
        meters.append(_new_meter(row, s.query(DailyConsumption).where(DailyConsumption.MeterID == row.MeterID).first()))

    if not meters:
        raise fastapi.HTTPException(404)



    return meters