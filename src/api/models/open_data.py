from pydantic import BaseModel

class LegalData(BaseModel):
    url: str | None

class TwoGisBranch(BaseModel):
    name: str
    purpose_name: str | None

class TwoGisData(BaseModel):
    url: str | None
    branches: list[TwoGisBranch] | None

class AvitoData(BaseModel):
    url: str
    title: str
    description: str