from fastapi import APIRouter
from fastapi.openapi.docs import get_swagger_ui_html

router = APIRouter()

@router.get("/docs")
def read_docs():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="FairWatt")