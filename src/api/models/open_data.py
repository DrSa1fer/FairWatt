from pydantic import BaseModel

class OpenData(BaseModel):
    avito_link: str | None
    is_legal_entity: bool
    is_bunch: bool