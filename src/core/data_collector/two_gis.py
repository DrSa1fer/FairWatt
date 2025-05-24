import requests
from .models import TwoGis

def companies_at_address(address: str, api_gis: str) -> list[TwoGis]:
    """
    Поиск компаний на адресе
    :param address: Полный адрес
    :param api_gis: API ключ 2gis - dev.2gis.ru

    :return list[TwoGis]: Список компаний если найдены
    """
    base_url = "https://catalog.api.2gis.com/3.0/"
    method = "items"

    response = requests.get(
        base_url +
        method +
        f"?key={api_gis}" +
        f"&q={address}" +
        "&locale=ru_RU" +
        "&type=branch" +
        "&fields=items.address"
    ).json()

    if response["meta"]["code"] == 200:
        result = []
        for item in response["result"]["items"]:
            print(item)
            result.append(
                TwoGis(
                    type_=item.get("type"),
                    name=item.get("name"),
                    purpose_name=item.get("purpose_name"),
                    building_id=item["address"]["building_id"],
                )
            )
        return result
    return []

def generate_map_for_building(building_id: str) -> str:
    """
    Сгенерировать ссылку на здание в 2gis
    :param building_id: 2gis id здания

    :return str: Ссылка на карту
    """
    return f"https://2gis.ru/geo/items/{building_id}"