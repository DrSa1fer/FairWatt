import os
import json
import tempfile
from matplotlib import pyplot
from typing import Optional
from pathlib import Path

def load_data(data_folder: Optional[Path] = None) -> list[dict]:
    if data_folder is None:
        data_folder = Path("../data")

    datasets = ["commercial.json", "personal.json"]
    result = []
    for dataset in datasets:
        with open(data_folder / Path(dataset), "r") as ds:
            result += json.loads(ds.read())

    return result


def generate_charts(save_to: Path):
    dataset = load_data()
    save_to = save_to / Path("FairWatt")
    os.mkdir(save_to)

    for id, consumption in enumerate(dataset):
        personal = consumption["rating"] <= 0.5
        pyplot.figure(figsize=(10, 6))
        pyplot.plot(range(24), consumption["consumption"], marker="o", linestyle="-", color="b" if personal else "r", label="кВт·ч")

        pyplot.title(f"{'Персональное' if personal else 'Коммерческое'} использование ({consumption['rating']})")
        pyplot.xlabel("Время")
        pyplot.ylabel("кВт·ч")
        pyplot.grid(True)
        pyplot.xticks(range(24))

        pyplot.savefig(save_to / Path(f"{id}.png"))
        pyplot.close()
    print(f"== Графики сохранены в '{save_to}' ==")

generate_charts(
    Path(
        tempfile.gettempdir()
    )
)
