from fastapi import APIRouter, HTTPException
from sqlalchemy import text

from sqlalchemy.orm import joinedload

from src.db.schemes.client import Client
from src.db.schemes.meter import Meter
from src.db.schemes.verified import Verified
from src.db.schemes.verified_grade import VerifiedGrade

from src.db.session import session

router = APIRouter(tags=["statistics"])

@router.get("/questionableClients")
async def questionable_client_count() -> int:
    grade_id = session().query(VerifiedGrade).filter(VerifiedGrade.Name == "Коммерческое").first().VerifiedGradeID

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
async def average_facility_consumption(is_iot : bool = False) -> float:
    result = session().execute(text((
    f"""
        SELECT (SELECT SUM(s) FROM UNNEST(c."Data") s) as x 
        FROM {'"DailyConsumption"' if not is_iot else '"MonthlyConsumption"'} c
        JOIN "Meter" m ON c."MeterID" = m."MeterID"
        JOIN "Facility" f ON f."FacilityID" = m."FacilityID"
        JOIN "FacilityKind" k ON k."FacilityKindID" = f."FacilityKindID"
        WHERE k."Name" = 'Частный';
    """
    ))).first()

    if result is None:
        return 0

    return result[0]


@router.get("/averageFlatConsumption")
async def average_flat_consumption(is_iot : bool = False) -> float:
    result = session().execute(text((
    f"""
        SELECT (SELECT SUM(s) FROM UNNEST(c."Data") s) as x 
        FROM {'"DailyConsumption"' if not is_iot else '"MonthlyConsumption"'} c
        JOIN "Meter" m ON c."MeterID" = m."MeterID"
        JOIN "Facility" f ON f."FacilityID" = m."FacilityID"
        JOIN "FacilityKind" k ON k."FacilityKindID" = f."FacilityKindID"
        WHERE k."Name" = 'Многоквартирный';
    """
    ))).first()

    if result is None:
        return 0

    return result[0]


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
