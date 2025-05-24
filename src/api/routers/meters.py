import random
from typing import List, Type

import fastapi
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from src.api.views.meter import Meter as AWMeter, MeterDetail, Geodata
from src.db.schemes.client import Client
from src.db.schemes.daily_consumption import DailyConsumption
from src.db.schemes.monthly_consumption import MonthlyConsumption
from src.db.schemes.facility import Facility
from src.db.schemes.meter import Meter as DBMeter
from src.db.schemes.tariff import Tariff
from src.db.schemes.verified import Verified
from src.db.session import session

router = APIRouter(tags=["meters"])

def _new_meter(s: Session, meter, consumption, is_daily) -> AWMeter:
    client: Client = meter.Client
    facility: Facility = meter.Facility
    verified: Verified | None = s.query(Verified).filter(Verified.FacilityID == facility.FacilityID).first()
    tariff: Tariff = meter.Tariff

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
            facility_type_name=facility.FacilityKind.Name,
            tariff_price=tariff.Price,
            tariff_type_name=tariff.TariffKind.Name
        ),
        geodata=Geodata(
            longitude=facility.Longitude,
            latitude=facility.Latitude
        ),
        consumption=consumption.Data if consumption is not None else None,
        is_daily=is_daily,
        is_first=None,
        verified_status=verified.Grade.Name if verified is not None else None
    )

def get_last_consumption(s: Session, meter_id: int) -> tuple[Type[DailyConsumption] | Type[MonthlyConsumption] | None, bool]:
    is_daily = True

    cons = (s.query(DailyConsumption)
            .filter(DailyConsumption.MeterID == meter_id)
            .order_by(DailyConsumption.Date.desc())
            .first())

    if not cons:
        is_daily = False
        cons = (s.query(MonthlyConsumption)
                .filter(MonthlyConsumption.MeterID == meter_id)
                .order_by(MonthlyConsumption.Date.desc())
                .first())

    return cons, is_daily

@router.get("/meter")
async def api_meter(meter_id: int) -> AWMeter | str:
    s = session()
    row = s.get(DBMeter, meter_id)

    if not row:
        raise HTTPException(status_code=404, detail="Meter not found")

    cons, is_daily = get_last_consumption(s, meter_id)

    return _new_meter(s, row, cons, is_daily)

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

    meters = []

    for row in (s.query(DBMeter).offset((page - 1) * per_page).limit(per_page)):
        cons, is_daily = get_last_consumption(s, row.MeterID)
        meters.append(_new_meter(s, row, cons, is_daily))

    return meters