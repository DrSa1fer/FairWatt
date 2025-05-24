import requests

def cords_of_address(address: str, api_ya_geocode: str) -> tuple[float, float]:
    """
    Поиск координат по адресу
    :param address: Полный адрес
    :param  api_ya_geocode: API ключ yandex геокодер - developer.tech.yandex.ru

    :return tuple[float]: Координаты или 0,0 при ошибке
    """
    base_url = "https://geocode-maps.yandex.ru/v1"

    response = requests.get(
        base_url +
        f"?apikey={api_ya_geocode}" +
        f"&geocode={address}" +
        "&format=json"
    )

    if response.status_code != 200:
        return (0,0) # TODO: Ошибка

    feature_member = response.json()["response"]["GeoObjectCollection"]["featureMember"]

    if not len(feature_member):
         return (0,0) # TODO: Ошибка

    x, y = feature_member[0]["GeoObject"]["Point"]["pos"].split()
    return (float(x), float(y))
