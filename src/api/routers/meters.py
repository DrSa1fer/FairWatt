import random
from typing import List, Union

import fastapi
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from src.db.schemes.facility import Facility as DBFacility
from src.db.schemes.client import Client as DBClient
from src.db.schemes.meter import Meter as DBMeter

from src.db.schemes.daily_consumption import DailyConsumption
from src.db.schemes.monthly_consumption import MonthlyConsumption
from src.db.schemes.tariff import Tariff

from src.api.views.meter import Meter as AWMeter, MeterDetail, Geodata, Client
from src.db.schemes.verified import Verified
from src.db.session import session

router = APIRouter(prefix="/meters", tags=["Meters"])


def _new_meter(s: Session, meter : AWMeter, consumption) -> AWMeter:
    client: DBClient = meter.Client
    facility: DBFacility = meter.Facility
    tariff: Tariff = meter.Tariff

    verified: Verified | None = s.query(Verified).filter(Verified.FacilityID == facility.FacilityID).first()

    return AWMeter(
        meter_id=meter.MeterID,
        facility_id=facility.FacilityID,
        rating=100 - (client.Rating * 100),
        address=facility.Address.rstrip(),
        notes=meter.Notes,
        meter_details=MeterDetail(
            resident_count=facility.Residents,
            room_count=facility.Rooms,
            square=facility.Square,
            facility_type_name=facility.FacilityKind.Name.rstrip(),
            tariff_price=tariff.Price,
            tariff_type_name=tariff.TariffKind.Name.rstrip()
        ),
        client=Client(
            client_id=client.ClientID,
            name=f"{client.LastName} {client.FirstName} {client.FatherName}",
            phone=client.Phone,
            email=client.Email.rstrip(),
        ),
        geodata=Geodata(
            longitude=facility.Longitude,
            latitude=facility.Latitude
        ),
        consumption=consumption.Data if consumption is not None else None,
        is_iot=meter.IsIot,
        is_first=None,
        verified_status=verified.Grade.Name if verified is not None else None
    )


@router.get("/{meter_id}")
async def api_meter(meter_id: int) -> AWMeter:
    try:
        s = session()
    except:
        raise fastapi.HTTPException(500)

    row = s.get(DBMeter, meter_id)

    if not row:
        raise HTTPException(status_code=404, detail="Meter not found")

    if row.IsIot:
        tmp = s.query(DailyConsumption).filter(DailyConsumption.MeterID == meter_id)
    else:
        tmp = s.query(MonthlyConsumption).filter(MonthlyConsumption.MeterID == meter_id)

    if not tmp:
        raise fastapi.HTTPException(404)

    return _new_meter(s, row, tmp.first())

@router.get("/")
@router.get("/list")
async def api_meters(page: int = 1, per_page: int = 10) -> List[AWMeter]:
    try:
        s = session()
    except RuntimeError:
        raise fastapi.HTTPException(500)

    if page < 1 or per_page < 1:
        raise fastapi.HTTPException(400)

    meters = []

    for row in (s.query(DBMeter).offset((page - 1) * per_page).limit(per_page)):
        if row.IsIot:
            tmp = s.query(DailyConsumption).filter(DailyConsumption.MeterID == row.MeterID)
        else:
            tmp = s.query(MonthlyConsumption).filter(MonthlyConsumption.MeterID == row.MeterID)

        if not tmp:
            raise fastapi.HTTPException(404)

        meters.append(_new_meter(s, row, tmp.first()))

    return meters




@router.put("/note")
def update_note(meter_id : int, notes : str):
    try:
        s = session()
    except RuntimeError:
        raise fastapi.HTTPException(500)

    tmp = s.get(DBMeter, meter_id)

    if not tmp:
        raise fastapi.HTTPException(404)

    tmp.Notes = notes
    s.commit()