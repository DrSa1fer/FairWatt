from typing import List
from fastapi import APIRouter, HTTPException

from src.api.models.meter import Meter as MeterModel, MeterDetails
from src.db.session import session as db_session
from src.db.schemes.daily_consumption import DailyConsumption as Consumption
from src.db.schemes.facility import Facility
from src.db.schemes.client import Client
from src.db.schemes.tariff import Tariff
from src.db.schemes.meter import Meter

router = APIRouter()

@router.get("/meter/{meter_id}")
async def api_meter(meter_id: int) -> MeterModel:
    session = db_session()
    meter = session.get(Meter, meter_id)
    if not meter:
        raise HTTPException(status_code=404, detail="Meter not found")

    client: Client = meter.Client
    facility: Facility = meter.Facility
    tariff: Tariff = meter.Tariff

    consumption = (
                    session.query(Consumption)
                    .filter(Consumption.MeterID == meter.MeterID)
                    .order_by(Consumption.Date.desc())
                    .first()
                   )

    return MeterModel(
        id = meter_id,
        name = f"{client.LastName} {client.FirstName} {client.FatherName}",
        rating = 100 - (client.Rating * 100),
        address = facility.Address,
        lastConsumption = 0, # todo
        tariffName = tariff.TariffKind.Name,
        tariffPrice = tariff.Price,
        meterDetails = MeterDetails(
            square = facility.Square,
            hasElectricHeating = facility.hasElectricHeating,
            hasElectricStove = facility.hasElectricStove,
            facilityName = facility.SettlementKind.Name,
        )

    )


@router.get("/meters")
async def api_meters(page: int = 0, per_page: int = 10) -> List[MeterModel]:
    session = db_session()

    offset = (page - 1) * per_page
    meters = []
    for meter in (session.query(Meter).offset(offset).limit(per_page)):
        client: Client = meter.Client
        facility: Facility = meter.Facility
        tariff: Tariff = meter.Tariff
        meters.append(
                MeterModel(
                id=meter.MeterID,
                name=f"{client.LastName} {client.FirstName} {client.FatherName}",
                rating=100 - (client.Rating * 100),
                address=facility.Address,
                lastConsumption=0,  # todo
                tariffName=tariff.TariffKind.Name,
                tariffPrice=tariff.Price,
                meterDetails=MeterDetails(
                    square=facility.Square,
                    hasElectricHeating=facility.hasElectricHeating,
                    hasElectricStove=facility.hasElectricStove,
                    facilityName=facility.SettlementKind.Name,
                    )
                )
        )


    return meters