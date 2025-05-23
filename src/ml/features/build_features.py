import numpy as np
import pandas as pd

def build_features(data : list[dict[str, str | int | float | dict[str, int]]]) -> (pd.DataFrame, pd.DataFrame):
    result = pd.DataFrame([dict
        (
            accountId=i["accountId"],
            isCommercial=i["isCommercial"],
            # address=i["address"],
            # buildingType=i["buildingType"],
            roomsCount=i["roomsCount"],
            residentsCount=i["residentsCount"],
            consumption_01=i["consumption"]["1"],
            consumption_02=i["consumption"]["2"],
            consumption_03=i["consumption"]["3"],
            consumption_04=i["consumption"]["4"],
            consumption_05=i["consumption"]["5"],
            consumption_06=i["consumption"]["6"],
            consumption_07=i["consumption"]["7"],
            consumption_08=i["consumption"]["8"],
            consumption_09=i["consumption"]["9"],
            consumption_10=i["consumption"]["10"],
            consumption_11=i["consumption"]["11"],
            consumption_12=i["consumption"]["12"],
        ) for i in data
    ])


    return result.drop("rating", axis=1), result["rating"]