from fastapi import FastAPI
from uvicorn import run

from src.api.routers import meters, employees
from src.config import Settings
from src.db.session import db_init, dispose, session
from fastapi.openapi.docs import get_swagger_ui_html

def main():
    config = Settings()

    db_init(config.pg_dsn)
    session().commit()

    app = FastAPI(
        title="FairWatt API",
        description="🏔️ A project to analyze energy consumption by Elbrus team",
    )




    app.include_router(meters.router, prefix="/api/v1")
    app.include_router(employees.router, prefix="/api/v1")

    run(app, host=config.api_host, port=config.api_port, reload=False)

    dispose() # dispose connection

main()