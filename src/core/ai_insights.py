from textwrap import dedent

from openai import OpenAI
from .data_collector.models import AdvertInfo
from json import dumps

def check_adverts(address: str, adverts: list[AdvertInfo], api_key: str, base_url: str, model: str) -> AdvertInfo | None:
    """
    Проверка найденных по адресу объявлений на коммерческую деятельность
    :param address: Полный адрес
    :param adverts: Найденные объявления
    :param api_key: API ключ
    :param base_url: API url
    :param model: Наименование LLM модели
s
    :return list[AdvertInfo]: Массив проверенных объявлений
    """

    client = OpenAI(
        api_key=api_key,
        base_url=base_url
    )

    input_data = {
        "address": address,
        "adverts": []
    }

    for advert in adverts:
        input_data["adverts"].append({
            "title": advert.title,
            "description": advert.description,
            "url": advert.url
        })


    response = client.chat.completions.create(
        messages=[
        {"role": "user", "content":
        dedent("""\
            Твоя задача обнаружить объекты, осуществляющие коммерческую детяльности. На вход тебе поступает адрес и краткая информация о найденных объявлениях на этом адресе.
            Например `{address: "<адрес>", "adverts": [{"title": "<Заголовок>", "description": "<Часть описания>", "url": "<Ссылка>"}]}`.
            Тебе необходимо проверить найденные объявления на подозрения в коммерческой деятельности на этом адресе, отсортировав обычную продажу товаров и неподходящие адреса.
            Так же нужно проверить точно ли данные объявления относятся к заданному адресу. Адрес может содержаться в заголовке, части описания и ссылке.
            В ответе ты должен отправить числовой индекс для `adverts`, где есть подозрения на коммерческую деятельность и они с большой вероятностью относятся к адресу в формате
            числа `1`, и НИКАК ИНАЧЕ!
            При любом исходе ты должен ответь одним числом, без любых комментариев. Если ничего не удалось найти или что-то пошло не так верни `-1`.
        """)},
        {"role": "user", "content": dumps(input_data)}],
        model=model,
        max_tokens=50000
    )

    try:
        index = int(response.choices[0].message.content)
    except TypeError:
        return None # TODO: Ошибка

    if index == -1:
        return None

    return adverts[index]
