import json

from src.ml.months.predict import predict, Data
from src.ml.months.train.train_model import train


with open("./months/data/test/dataset_control.json") as f:
    data = json.load(f)

X = [
    Data(
        buildingType=
        0 if i["buildingType"] == "Частный" else
        1 if i["buildingType"] == "Прочий" else
        2,

        consumption     =i["consumption"],
        totalArea       =i.get("totalArea"),
        roomsCount      =i.get("roomsCount"),
        residentsCount  =i.get("residentsCount"),
    ) for i in data]
y = predict(X)
y = y.tolist()


for i in range(len(y)):
    data[i]["rating"] = y[i]
    # data[i]["isCommercial"] = y[i] > 0.5


with open("rate_data.json", "w+", encoding='utf8') as f:
    f.write(json.dumps(data, ensure_ascii=False))

print(data)