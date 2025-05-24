from googlesearch import search
from .models import AdvertInfo

def find_avito_adverts_by_address(address: str, max_results_to_check: int) -> list[AdvertInfo]:
    """
    Поиск координат по адресу
    :param address: Полный адрес
    :param max_results_to_check: Количество результатов в выдаче, которые нужно проверить на наличие объявлений

    :return list[AdvertInfo]: Массив найденных объявлений
    """
    result_adverts: list[AdvertInfo] = []

    for result in search(f"site:avito.ru {address}", max_results_to_check, "ru", safe=False, advanced=True):
        url = result.url
        if str.isnumeric(url.rsplit("_")[-1]):
            result_adverts.append(
                AdvertInfo(
                    title=result.title,
                    description=result.description,
                    url=url
                )
            )

    return result_adverts
