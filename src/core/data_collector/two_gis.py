import requests
from models import TwoGis

def companies_at_address(address: str, api_gis: str) -> list[TwoGis]:
    """
    Поиск компаний на адресе
    :param address: Полный адрес
    :param  api_gis: API ключ 2gis - dev.2gis.ru

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
        "&type=branch"
    ).json()

    if response["meta"]["code"] == 200:
        result = []
        for item in response["result"]["items"]:
            result.append(
                TwoGis(
                    type_=item.get("type"),
                    purpose_name=item.get("purpose_name")
                )
            )
        return result
    return []
