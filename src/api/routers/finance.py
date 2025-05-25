from fastapi import APIRouter
from src.db.session import session
from src.db.schemes.meter import Meter

router = APIRouter(tags=["finance"])

@router.get("/calculateLosses")
def calculate_losses(meter_id: int) -> float:
    s = session()
    meter = s.get(Meter, (meter_id,))
    in_fact = 0
    need_be = 0

    return 0