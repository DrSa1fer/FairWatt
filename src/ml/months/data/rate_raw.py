import json
import statistics
from os import write

with open("train/raw_train.json") as f:
    data = json.load(f)


def clamp(value, _min, _max):
    return max(min(value, _max), _min)

# Функция для нормализации значений в диапазон [0, 1]
def normalize(value, min_val, max_val):
    if max_val == min_val:  # Избегаем деления на ноль
        return 0
    return clamp ((value - min_val) / (max_val - min_val), 0, 1)


# Функция для расчета рейтинга
def calculate_commercial_score(record):
    # Извлечение параметров
    rooms_count = record.get("roomsCount", None)
    residents_count = record.get("residentsCount", None)
    consumption = [int(v) for v in record["consumption"].values()]
    total_area = record.get("totalArea", None)

    # Параметры для нормализации
    max_rooms = 7  # Предполагаемый максимум комнат
    max_residents = 6  # Предполагаемый максимум жильцов
    max_consumption = 3000  # Максимальное месячное потребление (кВт·ч)
    max_consumption_per_area = 40  # Максимальное потребление на м² (кВт·ч/м²)
    max_area = 200  # Максимальная площадь (м²)
    max_cv = 1.0  # Максимальный коэффициент вариации

    # Инициализация оценок и весов
    scores = {
    }
    weights = {
        "rooms": 0.3,  # Веса: комнаты имеют умеренную значимость
        "residents": 0.3,  # Веса: жильцы имеют высокую значимость
        "consumption": 0.3,  # Веса: потребление - ключевой фактор
        "cv": 0.2,  # Веса: стабильность потребления важна
        "area": 0.2,  # Веса: потребление на площадь важно, если доступно
    }

    # 3. Оценка по потреблению электроэнергии
    # Высокое среднее потребление -> выше вероятность коммерческого использования
    avg_consumption = statistics.mean(consumption)
    scores["consumption"] = normalize(avg_consumption, 0, max_consumption)

    # 1. Оценка по количеству комнат
    if rooms_count is not None:
        consumption_per_rooms = avg_consumption / rooms_count
        scores["rooms"] = (1 - #normalize(consumption_per_rooms, 1, max_consumption_per_rooms) *
                           normalize(rooms_count, 1, max_rooms))
    else:
        weights["rooms"] = 0

    # 2. Оценка по количеству жильцов
    if residents_count is not None:
        consumption_per_resident = avg_consumption / residents_count
        scores["residents"] = (1 - #normalize(consumption_per_resident, 1, max_consumption_per_residents) *
                               normalize(residents_count, 1, max_residents))
    else:
        weights["residents"] = 0

    if total_area:
        consumption_per_area = avg_consumption / total_area
        scores["area"] = normalize(consumption_per_area, 0, max_consumption_per_area)
    else:
        weights["area"] = 0

    # 4. Оценка по стабильности потребления (коэффициент вариации)
    # Низкая вариативность -> выше вероятность коммерческого использования
    std_dev = statistics.stdev(consumption) if len(consumption) > 1 else 0
    mean_cons = avg_consumption if avg_consumption > 0 else 1  # Избегаем деления на ноль
    cv = std_dev / mean_cons
    scores["cv"] = 1 - normalize(cv, 0, max_cv)

    # 5. Оценка по потреблению на единицу площади

    # Суммирование взвешенных оценок
    total_score = sum(scores[key] * weights[key] for key in scores)
    total_weight = sum(weights.values())

    # Нормализация и масштабирование до [0, 100]
    final_score = (total_score / total_weight) * 100 if total_weight > 0 else 0

    if record["isCommercial"]:
        final_score *= 1.2

    return round(final_score, 2)


# Применение алгоритма к данным
for record in data:
    score = calculate_commercial_score(record)
    print(f"{record | {'score': score}}")

