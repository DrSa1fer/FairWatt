from fastapi import APIRouter
from src.api.models.open_data import LegalData, TwoGisData, AvitoData, TwoGisBranch
from src.config import config
from src.core.data_collector.fns import check_legal_entity
from src.core.data_collector.models import TwoGis, AdvertInfo
from src.core.data_collector.two_gis import companies_at_address
from src.core.data_collector.two_gis import generate_map_for_building
from src.core.data_collector.avito import find_avito_adverts_by_address
from src.core.ai_insights import check_adverts

router = APIRouter(prefix="/dataCollect", tags=["Data Collector"])

@router.get("/legal")
async def data_collect_legal(full_name: str) -> LegalData:
    is_legal_entity, legal_url = check_legal_entity(full_name) if len(full_name) != 0 else (False, None)
    return LegalData(url=legal_url)


@router.get("/2gis")
async def data_collect_2gis(address: str) -> TwoGisData:
    companies: list[TwoGis] = companies_at_address(address, config.gis_api)

    branches: list[TwoGisBranch] = []

    if len(companies) == 0:
        return TwoGisData(url=None, branches=None)

    for company in companies:
        branches.append(TwoGisBranch(
            name=company.name,
            purpose_name=company.purpose_name
        ))

    return TwoGisData(url=generate_map_for_building(companies[0].building_id), branches=branches)


@router.get("/avito")
async def data_collect_avito(address: str) -> list[AvitoData]:
    if len(address) == 0:
        return []

    adverts: list[AdvertInfo] = find_avito_adverts_by_address(address, 10)

    filtered_advert = check_adverts(address, adverts, config.ai_api, config.ai_base_url, config.ai_model)

    results: list[AvitoData] = []

    if not filtered_advert: # Если что-то не так с ИИ
        for advert in adverts:
            results.append(AvitoData(
                url=advert.url,
                title=advert.title,
                description=advert.description,
            ))

        return results


    results.append(AvitoData(
        url=filtered_advert.url,
        title=filtered_advert.title,
        description=filtered_advert.description,
    ))

    return results