from fastapi import APIRouter

from src.api.views.train import Train
from src.ml.days.train.train_model import train as ttraing

router = APIRouter(prefix="ml", tags=["ML"])

@router.get("/train")
async def train(train : Train) -> None:
    ttraing()