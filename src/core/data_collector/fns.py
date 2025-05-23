import requests
from bs4 import BeautifulSoup
from fake_headers import Headers

def is_legal_entity(full_name: str) -> bool:
    """
    Поиск юридических лиц в системе ФНС
    :param full_name: ФИО
    :return: Найдены ли данные в системы ФНС

    ! На основе этих данных, можно только предположить
    о наличии юридического лица у человека.
    Учитывайте, что реализация через скрапинг
    - временная. Для постоянного решения необходимо
    получить офицальный API ФНС.
    """
    base_url = "https://www.list-org.com/"
    method = "search"
    try:
        response = requests.get(
            base_url + method +
            f"?val={full_name.strip().replace(' ', '+')}" +
            "&work=on",
            headers=Headers().generate()
        ).text
    except requests.RequestException as exc:
        return False

    bs4 = BeautifulSoup(response, "lxml")
    bs4.find_all("div", class_="org_list")

    return bool(bs4.find_all("div", class_="org_list"))
