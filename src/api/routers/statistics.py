from fastapi import APIRouter, HTTPException

from sqlalchemy.orm import joinedload

from src.db.schemes.client import Client
from src.db.schemes.meter import Meter
from src.db.schemes.verified import Verified
from src.db.schemes.verified_grade import VerifiedGrade
from src.db.schemes.facility import Facility
from src.db.schemes.daily_consumption import DailyConsumption
from src.db.schemes.monthly_consumption import MonthlyConsumption

from src.db.session import session

router = APIRouter(tags=["statistics"])

@router.get("/questionableClients")
async def questionable_client_count() -> int:
    # TODO: Проверить имя в БД
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
async def average_facility_consumption() -> float:
    s = session()

    facilities = s.query(Facility).options(joinedload(Facility.Meters)).all()
    facility_averages = []

    for facility in facilities:
        meters = facility.Meters or []
        meter_averages = []

        for meter in meters:
            cons_model = DailyConsumption if meter.IsIot else MonthlyConsumption
            latest_cons = (
                s.query(cons_model)
                .filter(cons_model.MeterID == meter.MeterID)
                .order_by(cons_model.Date.desc())
                .first()
            )
            if not latest_cons:
                continue
            avg_consumption = sum(latest_cons.Data) / len(latest_cons.Data)
            meter_averages.append(avg_consumption)

        if meter_averages:
            facility_averages.append(sum(meter_averages) / len(meter_averages))

    return (sum(facility_averages) / len(facility_averages)) if facility_averages else 0.0



@router.get("/averageFlatConsumption/{facility_id}")
async def average_flat_consumption(facility_id: int) -> float:
    s = session()

    facility = (
        s.query(Facility)
        .options(joinedload(Facility.Meters))
        .filter(Facility.FacilityID == facility_id)
        .first()
    )
    if not facility:
        raise HTTPException(status_code=404, detail="Facility not found")

    meter_averages = []
    for meter in facility.Meters:
        cons_model = DailyConsumption if meter.IsIot else MonthlyConsumption
        latest_cons = (
            s.query(cons_model)
            .filter(cons_model.MeterID == meter.MeterID)
            .order_by(cons_model.Date.desc())
            .first()
        )
        if not latest_cons or not latest_cons.Data:
            continue
        avg_consumption = sum(latest_cons.Data) / len(latest_cons.Data)
        meter_averages.append(avg_consumption)

    return (sum(meter_averages) / len(meter_averages)) if meter_averages else 0.0

@router.get("/averageMonthConsumption")
async def average_month_consumption() -> list[float]:
    s = session()
    months = 12
    result = [0.0] * months
    result_counts = [0] * months

    meters = (
        s.query(Meter)
        .filter(~Meter.IsIot)
        .options(joinedload(Meter.MonthlyConsumptions))
        .all()
    )

    for meter in meters:
        for cons in meter.MonthlyConsumptions:
            data = cons.Data or []
            for i, val in enumerate(data):
                if i < months:
                    result[i] += val
                    result_counts[i] += 1

    averages = [
        (result[i] / result_counts[i]) if result_counts[i] > 0 else 0.0
        for i in range(months)
    ]
    return averages
