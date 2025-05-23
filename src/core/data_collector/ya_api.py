import requests

def cords_of_address(address: str, api_ya_geocode: str) -> str:
    """
    Поиск координат по адресу
    :param address: Полный адрес
    :param  api_ya_geocode: API ключ yandex геокодер - developer.tech.yandex.ru

    :return str: Координаты или 0,0 при ошибке
    """
    base_url = "https://geocode-maps.yandex.ru/"
    method = "v1"

    response = requests.get(
        base_url +
        method +
        f"?apikey={api_ya_geocode}" +
        f"&geocode={address}" +
        "&format=json"
    )

    if response.status_code != 200:
        return "0,0" # TODO: Ошибка

    json = response.json()["response"]["GeoObjectCollection"]["featureMember"]

    if len(json) == 0:
         return "0,0" # TODO: Ошибка

    return str(json[0]["GeoObject"]["Point"]["pos"]).replace(" ", ",")


def panorama_url_by_address(address: str, api_ya_geocode: str) -> str:
    """
    Создание ссылки на панорамы яндекс карт по адресу
    :param address: Полный адрес
    :param  api_ya_geocode: API ключ yandex геокодер - developer.tech.yandex.ru

    :return str: Ссылка или yandex.ru при ошибке
    """

    pos = cords_of_address(address, api_ya_geocode)
    if pos == "0,0": # TODO: Нормальная ошибка и её обработка
        return "https://yandex.ru"

    base_url = "https://yandex.ru/"
    method = "maps"

    return (base_url +
            method +
            f"?l=stv,sta" +
            f"&ll={pos}" +
            "&panorama[direction]=0.000000,0.000000" +
            "&panorama[full]=true" +
            f"&panorama[point]={pos}" +
            "&panorama[span]=120.692570,60.000000" +
            "&z=18"
            )

