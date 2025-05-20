import json
import tempfile
from matplotlib import pyplot
from pathlib import Path
from typing import Optional

def load_data(data_folder: Optional[Path] = None) -> list[dict]:
    if data_folder is None:
        data_folder = Path("src/data")

    datasets = ["commercial.json", "personal.json"]
    result = []
    for dataset in datasets:
        with open(data_folder / Path(dataset), "r") as ds:
            result += json.loads(ds.read())

    return result


def main(save_to: Path):
    dataset = load_data()
    hours = list(range(24))

    for id, consumption in enumerate(dataset):
        personal = consumption["rating"] <= 0.5
        pyplot.figure(figsize=(10, 6))
        pyplot.plot(hours, consumption["consumption"], marker="o", linestyle="-", color="b" if personal else "r", label="кВт·ч")

        pyplot.title(f"{'Personal' if personal else 'Commercial'} ({consumption['rating']})")
        pyplot.xlabel("Время")
        pyplot.ylabel("кВт·ч")
        pyplot.grid(True)
        pyplot.xticks(hours)

        pyplot.savefig(save_to / Path(f"{id}.png"))
        pyplot.close()
    print(f"== Графики сохранены в '{save_to}' ==")

main(Path(
    tempfile.gettempdir()
))
