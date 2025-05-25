from fastapi import FastAPI
from sqlalchemy import text
from uvicorn import run

from src.api.routers import meters, employees, trips, data_collector, statistics, finance
from src.config import config
from src.db.session import init, dispose, session


def main():
    init(config.pg_dsn)

    app = FastAPI(
        title="FairWatt API",
        description="🏔️ A project to analyze energy consumption by Elbrus team",
    )

    app.include_router(trips.router, prefix="/api/v1")
    app.include_router(data_collector.router, prefix="/api/v1")
    app.include_router(meters.router, prefix="/api/v1")
    app.include_router(employees.router, prefix="/api/v1")
    app.include_router(finance.router, prefix="/api/v1")

    run(app, host=config.api_host, port=config.api_port, reload=False)

    dispose() # dispose connection

main()