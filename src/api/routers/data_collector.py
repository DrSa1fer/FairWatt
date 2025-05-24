from fastapi import APIRouter
from src.api.models.open_data import OpenData
from src.config import config

router = APIRouter()

@router.get("/dataCollect")
async def data_collect(full_name: str, address: str) -> OpenData:
    pass

