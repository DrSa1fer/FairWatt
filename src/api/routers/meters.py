import random
from typing import List, Type

import fastapi
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from src.api.views.meter import Meter as AWMeter, MeterDetail, Geodata, Client
from src.db.schemes.client import Client as DBClient
from src.db.schemes.daily_consumption import DailyConsumption
from src.db.schemes.monthly_consumption import MonthlyConsumption
from src.db.schemes.facility import Facility
from src.db.schemes.meter import Meter as DBMeter
from src.db.schemes.tariff import Tariff
from src.db.schemes.verified import Verified
from src.db.session import session

router = APIRouter(tags=["meters"])

def _new_meter(s: Session, meter, consumption) -> AWMeter:
    client: DBClient = meter.Client
    facility: Facility = meter.Facility
    verified: Verified | None = s.query(Verified).filter(Verified.FacilityID == facility.FacilityID).first()
    tariff: Tariff = meter.Tariff

    return AWMeter(
        meter_id=meter.MeterID,
        facility_id=facility.FacilityID,
        rating=100 - (client.Rating * 100),
        address=facility.Address.strip(),
        meter_details=MeterDetail(
            resident_count=facility.Residents,
            room_count=facility.Rooms,
            square=facility.Square,
            facility_type_name=facility.FacilityKind.Name.strip(),
            tariff_price=tariff.Price,
            tariff_type_name=tariff.TariffKind.Name.strip()
        ),
        client=Client(
            client_id=client.ClientID,
            name=f"{client.LastName} {client.FirstName} {client.FatherName}",
            phone=str(client.Phone),
            email=client.Email
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

def get_last_consumption(s: Session, meter_id: int, is_iot: bool) -> Type[DailyConsumption] | Type[MonthlyConsumption] | None:
    return \
        (s.query(MonthlyConsumption).filter(MonthlyConsumption.MeterID == meter_id).order_by(MonthlyConsumption.Date.desc()).first()) \
        if is_iot else \
        (s.query(DailyConsumption).filter(DailyConsumption.MeterID == meter_id).order_by(DailyConsumption.Date.desc()).first())

@router.get("/meters/{meter_id}")
async def api_meter(meter_id: int) -> AWMeter | str:
    s = session()
    row: DBMeter = s.get(DBMeter, meter_id)

    if not row:
        raise HTTPException(status_code=404, detail="Meter not found")

    cons = get_last_consumption(s, meter_id, row.IsIot)

    return _new_meter(s, row, cons)

@router.get("/meters")
async def api_meters(page: int = 1, per_page: int = 10) -> List[AWMeter]:
    if random.randint(0, 1000000) == 418:
        raise fastapi.HTTPException(418, "U win!")

    try:
        s = session()
    except RuntimeError:
        raise fastapi.HTTPException(500)

    if page < 1 or per_page < 1:
        raise fastapi.HTTPException(400)

    meters: List[AWMeter] = []

    for row in s.query(DBMeter).offset((page - 1) * per_page).limit(per_page).all():
        cons = get_last_consumption(s, row.MeterID, row.IsIot)
        meters.append(_new_meter(s, row, cons))

    return meters