from fastapi import FastAPI
from uvicorn import run

from src.api.routers import meters
from src.db.session import global_init

def main():
    global_init("sqlite:///db.db") # What the hell?

    app = FastAPI(
        title="FairWatt API",
        description="🏔️ A project to analyze energy consumption by Elbrus team",
    )
    app.include_router(meters.router, prefix="/api/v1")

    run(app)

main()
