import json
from re import match


def json_to_sql():

    r = 'INSERT INTO "Facility"("FacilityID", "FacilityKindID", "Rooms", "Residents", "Square", "Address") VALUES\n'

    with open("raw_test.json") as f:
        data = json.load(f)[:1000:]

    for i in data:
        r += (f'({i["accountId"]}, '
              f' {"NULL" if i.get("buildingType", None) is None else 0 if i["buildingType"] == "Частный" else 1 if i["buildingType"] == "Прочий" else 2},'
              f' {"NULL" if i.get("roomsCount", None) is None else i["roomsCount"]}, '
              f' {"NULL" if i.get("residentsCount", None) is None else i["residentsCount"]}, '
              f' {"NULL" if i.get("totalArea", None) is None else i["totalArea"]}, '
              f' \'{i["address"].strip()}\'),\n')

    print(r)

json_to_sql()
