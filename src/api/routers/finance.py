from fastapi import APIRouter
from src.db.session import session
from src.db.schemes.meter import Meter
from src.db.schemes.daily_consumption import DailyConsumption
from src.db.schemes.monthly_consumption import MonthlyConsumption
from src.db.schemes.tariff import Tariff
from src.db.schemes.tariff_kind import TariffKind

router = APIRouter(tags=["finance"])

@router.get("/calculateLosses")
def calculate_losses(meter_id: int) -> float:
    s = session()
    meter = s.get(Meter, meter_id)

    if not meter:
        return 0.0

    current_price = meter.Tariff.Price
    target_price = (
        s.query(Tariff.Price)
        .filter(
            Tariff.TariffKindID == s.query(TariffKind.TariffKindID)
            .filter(TariffKind.Name == "Коммерческий")
            .scalar_subquery()
        )
        .scalar()
    )

    month_current = 0
    month_target = 0

    if meter.IsIot:
        for daily in (s.query(DailyConsumption)
         .filter(DailyConsumption.MeterID == meter.MeterID)
         .order_by(DailyConsumption.Date.desc()).limit(30).all()):
            data = daily.Data
            day = (sum(data) / len(data))
            month_current += day * current_price
            month_target += day * target_price
    else:
        month = (s.query(MonthlyConsumption)
             .filter(MonthlyConsumption.MeterID == meter.MeterID)
             .order_by(MonthlyConsumption.Date.desc())
             .first())
        if not month:
            return 0.0
        month = month.Data[-1]
        month_current = month * current_price
        month_target = month * target_price


    return abs(month_target - month_current)