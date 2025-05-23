from math import sqrt, pow
from typing import Annotated

Consume = Annotated[list[float], 24]

# utils
def avg(consume : Consume) -> float:
    if not len(consume):
        return 0
    return sum(consume) / len(consume)

# calculations
def calc_load_factor(consume : Consume) -> float:
    """
    Коэффициент заполненности графика
    :param consume: График потребления энергии за день
    :return: Потребление: LF > 70% - равномерное; LF < 30% - пиковое;
    """
    return avg(consume) / max(consume)
def calc_form_factor(consume : Consume) -> float:
    """
    Коэффициент формы графика
    :param consume: График потребления энергии за день
    :return: Потребление: FF ~~ 100% - постоянное; FF > 120% - колебания;
    """
    return sqrt(avg([pow(i, 2) for i in consume])) / avg(consume)
def calc_variation_index(consume : Consume) -> float:
    """
    Коэффициент вариации индекса графика
    :param consume: График потребления энергии за день
    :return: Потребление: VI ~~ 0% - постоянное; VI > 30% - колебания;
    """
    return sqrt(avg([pow(i - avg(consume), 2) for i in consume])) / avg(consume)

# analyze
def analyze(consume : Consume, perfect : Consume) -> float:
    """
    Быстрая оценка честности клиента
    :param consume: График потребления энергии за день
    :param perfect: График идеального потребления энергии за день
    :return: Рейтинг потребления от 0 до 100
    """
    vi = calc_variation_index(consume)  * 0.2   # coefficient
    lf = calc_load_factor(consume)      * 0.6   # coefficient
    ff = calc_form_factor(consume)      * 1.0   # coefficient

    rating = (1 - vi) * lf * ff * 100.0

    coefficient = 1
    for i in range(24):
        if consume[i] <= perfect[i]:
            continue
        coefficient += (consume[i] - perfect[i]) / consume[i] * 0.1

    rating *= coefficient

    if rating > 100:
        return 100

    if rating < 0:
        return 0

    return rating

def avg_analyze(consume : Consume, perfect : list[Consume]) -> float:
    return avg([analyze(consume, i) for i in perfect])