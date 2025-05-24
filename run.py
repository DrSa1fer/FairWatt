from fastapi import FastAPI
from uvicorn import run

from src.api.routers import meters
from src.api.routers import employees
from src.db.session import init, dispose


def main():
    init("postgresql+psycopg2://postgres:1234@localhost:5432/FairWattDB") # init connection

    app = FastAPI(
        title="FairWatt API",
        description="🏔️ A project to analyze energy consumption by Elbrus team",
    )
    app.include_router(meters.router, prefix="/api/v1")
    app.include_router(employees.router, prefix="/api/v1")

    run(app, host="0.0.0.0", port=8000, reload=False)

    dispose() # dispose connection

main()
