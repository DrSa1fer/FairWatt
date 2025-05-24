from days.predict import predict as dp, Data as dd
from months.predict import predict as mp, Data as md


class Day(dd):
    pass

def predict_by_days(data : list[Day]) -> list[float]:
    return dp(data)

class Month(md):
    pass

def predict_by_months(data : list[Month]) -> list[float]:
    return mp(data)
