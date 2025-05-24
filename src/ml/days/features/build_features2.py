import numpy as np
import pandas as pd


def build_features2(data : list[dict[str, str | int | float | dict[str, int]]]) -> (np.array, pd.DataFrame):
   result = dict()

   for i in ["Residents", "Square", "Rooms"]:
      result[f"{i}"] = [d.get(i, 0) for d in data]
      result[f"{i}_has"] = [d.get(i, None) is not None for d in data]

   for i in range(0, 24):
      result[f"consumption_{i+1}"] = [d["Consumption"][i] for d in data]
      result[f"consumption_{i+1}_has"] = [d["Consumption"][i] is not None for d in data]

   df = pd.DataFrame(result)

   return df.to_numpy(), np.array([d["rating"] for d in data]).ravel()