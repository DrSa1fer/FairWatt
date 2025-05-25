from fastapi import FastAPI
from uvicorn import run

from src.api.routers import meters, employees, trips, data_collector, statistics, finance
from src.config import config
from src.db.session import init, dispose
from fastapi.middleware.cors import CORSMiddleware


def main():
    init(config.pg_dsn)

    app = FastAPI(
        title="FairWatt API",
        description="🏔️ A project to analyze energy consumption by Elbrus team",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    app.include_router(trips.router, prefix="/api/v1")
    app.include_router(data_collector.router, prefix="/api/v1")
    app.include_router(meters.router, prefix="/api/v1")
    app.include_router(employees.router, prefix="/api/v1")
    app.include_router(finance.router, prefix="/api/v1")
    app.include_router(statistics.router, prefix="/api/v1")

    run(app, host=config.api_host, port=config.api_port, reload=False)

    dispose() # dispose connection

main()