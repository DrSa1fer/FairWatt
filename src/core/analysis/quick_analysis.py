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

# todo
# find perfect chart to analyze

#tests
# data0 = [0.45, 0.41, 0.38, 0.34, 0.39, 0.45, 1.89, 2.78, 3.34, 2.56, 2.01, 1.67, 1.45, 1.23, 1.12, 1.45, 2.34, 3.45, 4.01, 3.78, 3.23, 2.56, 1.67, 1.12]
# data1 = [2.89, 2.78, 2.67, 2.56, 2.45, 2.78, 3.56, 7.12, 13.45, 18.12, 20.34, 21.56, 21.23, 20.89, 20.12, 18.78, 17.12, 15.34, 13.12, 10.45, 7.89, 5.34, 3.78, 2.89]

# print("\n[load factor]:")
# print("personal = {", calc_load_factor(data0), "}")
# print("commercial = {", calc_load_factor(data1), "}")
#
# print("\n[form factor]:")
# print("personal = {", calc_form_factor(data0), "}")
# print("commercial = {", calc_form_factor(data1), "}")
#
# print("\n[variation index]:")
# print("personal = {", calc_variation_index(data0), "}")
# print("commercial = {", calc_variation_index(data1), "}")
#
# print("\n[analyze]:")
# print("personal = {", analyze(data0, data0), "}, must be 0.45")
# print("commercial = {", analyze(data1, data0), "}, must be 0.95")