from pydantic import BaseModel

class LegalData(BaseModel):
    url: str | None

class TwoGisData(BaseModel):
    url: str
    name: str
    purpose_name: str | None

class AvitoData(BaseModel):
    url: str
    title: str
    description: str