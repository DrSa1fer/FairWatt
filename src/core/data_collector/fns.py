import requests
from bs4 import BeautifulSoup
from fake_headers import Headers

def check_legal_entity(full_name: str) -> tuple[bool, str | None]:
    """
    Поиск юридических лиц в системе ФНС
    :param full_name: ФИО
    :return: Найдены ли данные в системы ФНС

    ! На основе этих данных, можно только предположить
    о наличии юридического лица у человека.
    Учитывайте, что реализация через скрапинг
    - временная. Для постоянного решения необходимо
    получить официальный API ФНС.
    """
    base_url = "https://www.list-org.com/"
    method = "search"

    target_url = (base_url + method +
            f"?val={full_name.strip().replace(' ', '+')}" +
            "&work=on")

    try:
        response = requests.get(
            target_url,
            headers=Headers().generate()
        ).text
    except requests.RequestException as exc:
        return False, None

    bs4 = BeautifulSoup(response, "lxml")
    bs4.find_all("div", class_="org_list")

    result = bool(bs4.find_all("div", class_="org_list"))

    return result, target_url if result else None
