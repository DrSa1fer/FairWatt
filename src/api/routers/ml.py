from fastapi import APIRouter

router = APIRouter(prefix="ml", tags=["ML"])

@router.get("/train")
async def train() -> None:
    pass