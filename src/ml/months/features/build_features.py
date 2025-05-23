import numpy as np
import pandas as pd

def build_features(data : list[dict[str, str | int | float | dict[str, int]]]) -> (np.array, pd.DataFrame):
    result = dict()

    for i in ["residentsCount", "totalArea", "roomsCount"]:
        result[f"{i}"] = [d.get(i, 0) for d in data]
        result[f"{i}_has"] = [d.get(i, None) is not None for d in data]

    for i in range(1, 13):
        result[f"consumption_{i}"]      = [d["consumption"].get(i, 0) for d in data]
        result[f"consumption_{i}_has"]  = [d["consumption"].get(i, None) is not None for d in data]

    df = pd.DataFrame(result)

    return df.to_numpy(), np.array([d["score"] for d in data]).ravel()
