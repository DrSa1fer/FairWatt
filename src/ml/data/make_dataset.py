import json
import pandas as pd
from pathlib import Path

from ..features.build_features import build_features

def make_dataset() -> pd.DataFrame:
    with open(Path("raw/test.json"), "r") as f:
        data = json.load(f)

    return build_features(data)
