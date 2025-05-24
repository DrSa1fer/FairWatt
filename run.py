from fastapi import FastAPI
from uvicorn import run

from src.api.routers import meters
from src.db.schemes.tariff_kind import TariffKind
from src.db.session import init, session, free

def main():
    init("postgresql+psycopg2://postgres:1234@localhost:5432/FairWattDB") # locally

    app = FastAPI(
        title="FairWatt API",
        description="🏔️ A project to analyze energy consumption by Elbrus team",
    )
    app.include_router(meters.router, prefix="/api/v1")

    run(app)
    free()

main()
