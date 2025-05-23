import os
import json
import tempfile
from pickletools import pylong

from matplotlib import pyplot
from typing import Optional
from pathlib import Path

def load_data(data_folder: Optional[Path] = None) -> list[dict]:
    if data_folder is None:
        data_folder = Path("../ml/months/data/test/")

    datasets = ["dataset_test.json"]
    result = []
    for dataset in datasets:
        with open(data_folder / Path(dataset), "r") as ds:
            result += json.loads(ds.read())

    return result


def generate_charts(save_to: Path):
    dataset = load_data()
    save_to = save_to / Path("FairWatt")

    # os.mkdir(save_to)

    for id, consumption in enumerate(dataset):
        pyplot.figure(figsize=(10, 6))
        pyplot.plot([i for i in consumption["consumption"].values()], marker="o", linestyle="-", color="r" if consumption['isCommercial'] else "b", label="кВт·ч")

        pyplot.title(f"Использование: {"Коммерческое" if consumption['isCommercial'] else "Частное"}\n" +
                     f"Тип жилья: {consumption.get('buildingType')}; " +
                     f"Кол-во комнат: {consumption.get('roomsCount')}; " +
                     f"Кол-во человек: {consumption.get('residentsCount')}; "
        )
        pyplot.xlabel("Месяц")
        pyplot.ylabel("кВт·ч")
        pyplot.grid(True)
        pyplot.xticks(range(12))

        pyplot.savefig(save_to / Path(f"{id}.png"))
        pyplot.close()
        if id == 200:
            break
    print(f"== Графики сохранены в '{save_to}' ==")

generate_charts(
    Path(
        tempfile.gettempdir()
    )
)
