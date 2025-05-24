from fastapi import APIRouter

from sqlalchemy.orm import joinedload

from src.db.schemes.client import Client
from src.db.schemes.meter import Meter
from src.db.schemes.verified import Verified
from src.db.schemes.verified_grade import VerifiedGrade
from src.db.schemes.facility import Facility

from src.db.session import session

router = APIRouter(tags=["statistics"])

@router.get("/questionableClients")
async def questionable_client_count() -> int:
    grade_id = session().query(VerifiedGrade).filter(VerifiedGrade.Name == "Коммерческое").fisrt().VerifiedGradeID

    return (session()
            .query(Client)
            .filter(Client.Rating > 70)
            .filter(
                ~session().query(Verified)
                .filter(
                    Verified.ClientID == Client.ClientID,
                    Verified.GradeID == grade_id
                ).exists()
    ).count())


@router.get("/averageFacilityConsumption")
async def average_facility_consumption(is_daily: bool = False) -> float:
    s = session()

    consumption_attr = 'DailyConsumptions' if is_daily else 'MonthlyConsumptions'

    sum_facilities = 0.0
    facilities = s.query(Facility).options(
        joinedload(Facility.Meters).joinedload(getattr(Meter, consumption_attr))
    ).all()

    facility_count = 0
    for facility in facilities:
        meters = facility.Meters
        if not meters:
            continue
        sum_meter = 0.0
        meter_count = 0
        for meter in meters:
            consumptions = getattr(meter, consumption_attr)
            if not consumptions:
                continue
            sum_consumption = 0.0
            for cons in consumptions:
                sum_consumption += sum(cons.Data) / len(cons.Data)
            sum_meter += sum_consumption / len(consumptions)
            meter_count += 1
        if meter_count > 0:
            sum_facilities += sum_meter / meter_count
            facility_count += 1

    return (sum_facilities / facility_count) if facility_count > 0 else 0.0



@router.get("/averageFlatConsumption/{facility_id}")
async def average_flat_consumption(facility_id: int, is_daily: bool = False) -> float:
    s = session()

    consumption_attr = 'DailyConsumptions' if is_daily else 'MonthlyConsumptions'

    facility = s.query(Facility).options(
        joinedload(Facility.Meters).joinedload(getattr(Meter, consumption_attr))
    ).filter(Facility.FacilityID == facility_id).first()

    if not facility or not facility.Meters:
        return 0.0

    sum_meter = 0.0
    meter_count = 0
    for meter in facility.Meters:
        consumptions = getattr(meter, consumption_attr)
        if not consumptions:
            continue
        sum_consumption = 0.0
        for cons in consumptions:
            if cons.Data:
                sum_consumption += sum(cons.Data) / len(cons.Data)
        sum_meter += sum_consumption / len(consumptions)
        meter_count += 1

    return (sum_meter / meter_count) if meter_count > 0 else 0.0

@router.get("/averageMonthConsumption")
async def average_month_consumption() -> list[float]:
    s = session()

    months = 12
    result = [0.0] * months
    result_counts = [0] * months

    # TODO: Как будет IOT, прогнать через ИИ
    # for m in s.query(Meter).filter(Meter.is_iot).all():

    for meter in s.query(Meter).all():
        for cons in meter.MonthlyConsumptions:
            data = cons.Data
            for i in range(0, len(data)):
                result[i] += data[i]
                result_counts[i] += 1

    for i in range(0, 12):
        result[i] /= result_counts[i]

    return result
