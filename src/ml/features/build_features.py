import numpy as np
import pandas as pd

def build_features(data : list[dict[str, str | int | float]]) -> (pd.DataFrame, pd.DataFrame):
    result = pd.DataFrame([dict(
        mean_consumption=np.mean(i["consumption_kwh"]),
        std_consumption=np.std(i["consumption_kwh"]),
        min_consumption=np.min(i["consumption_kwh"]),
        max_consumption=np.max(i["consumption_kwh"]),
        median_consumption=np.median(i["consumption_kwh"]),
        electric_stove=i["electric_stove"],
        electric_heating=i["electric_heating"],
        house_apartment=i["house_apartment"],
        rating=i["rating"]) for i in data
    ])

    return result.drop("rating", axis=1), result["rating"]