from typing import Type

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from data import db_session
from data.client import Client
from data.meter import Meter
from data.facility import Facility
from data.consumption import Consumption
from data.tariff import Tariff
from data.region import Region
from datetime import datetime, timedelta, timezone
app = FastAPI()

def generate_error(msg: str):
    return JSONResponse({"error": msg}, status_code=418)

def serialize_meter(meter: Type[Meter], session: Session):
    client: Client = meter.Client
    facility: Facility = meter.Facility
    tariff: Tariff = meter.Tariff
    region: Region = facility.Region

    consumption: Consumption = session.query(Consumption).filter(Consumption.MeterID == meter.MeterID).order_by(Consumption.Date.desc()).first()

    return {
        "id": meter.MeterID,
        "name": f"{client.LastName} {client.FirstName} {client.FatherName}",
        "rating": client.Rating,
        "address": facility.Address,
        "lastConsumption": consumption.Data[datetime.now(timezone(timedelta(hours=3))).hour] if consumption is not None else 0,
        "tariffName": tariff.TariffKind.Name,
        "tariffPrice": tariff.Price,
        "region": region.Name,
        "meterDetails": {
            "square": facility.Square,
            "hasElectricHeating": facility.hasElectricHeating,
            "hasElectricStove": facility.hasElectricStove,
            "facilityName": facility.FacilityKind.Name,
            "settlementName": facility.SettlementKind.Name
        }
    }

@app.get("/api/meter/{meter_id}")
async def api_meter(meter_id: int):

    session = db_session.create_session()

    meter = session.get(Meter, meter_id)

    if meter is None:
        return generate_error("Fail to get meter by id")

    return serialize_meter(meter, session)

@app.get("/api/meters")
async def api_meters():

    session = db_session.create_session()

    meters = session.query(Meter).all()

    r_meters = []
    for meter in meters:
        r_meters.append(serialize_meter(meter, session))

    return r_meters


def main():
    db_session.global_init(f"sqlite:///db.db")


main()
