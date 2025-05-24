from openai import OpenAI
from data_collector.models import AdvertInfo
from ast import literal_eval
from json import dumps
import collections.abc

def check_adverts(address: str, adverts: list[AdvertInfo], api_key: str) -> list[AdvertInfo]:
    """
    Проверка найденных по адресу объявлений на коммерческую деятельность
    :param address: Полный адрес
    :param adverts: Найденные объявления
    :param api_key: API ключ

    :return list[AdvertInfo]: Массив проверенных объявлений
    """

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.aitunnel.ru/v1/"
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
"""
На вход тебе поступает адрес и краткая информация о найденных объявлениях на этом адресе.
В формате `{address: "адрес", "adverts": [{"title": "Заголовок", "description": "Часть описания", "url": "Ссылка"}]}`.
Твоя задача проверить найденные объявления на наличие коммерческой деятельности, отсортировав обычную продажу товаров.
Так же нужно проверить точно ли данные объявления относятся к заданному адресу. Адрес может содержаться в заголовке, части описания и ссылке.
На выход ты должен отправить индексы `adverts` в которых ведётся коммерческая деятельность и они с большой вероятностью относятся к адресу в формате `[0, 3, ..]`.
При любом исходе ты должен отправить массив в python формате `[0, 3, ..]`, без любых комментариев.
"""},
        {"role": "user", "content": dumps(input_data)}],
        model="deepseek-chat-v3-0324",
        max_tokens=50000
    )

    try:
        indexes_array = literal_eval(str(response.choices[0].message.content))
    except SyntaxError:
        return adverts  # TODO: Ошибка

    if isinstance(indexes_array, collections.abc.Sequence):
        return adverts # TODO: Ошибка

    result: list[AdvertInfo] = []

    for index in indexes_array:
        result.append(adverts[index])

    return result