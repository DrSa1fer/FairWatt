from months.predict import predict as mp, Data as md


class Hour():
    pass

def predict_by_hours(data : list[dict]) -> list[float]:
    pass

class Day():
    pass

def predict_by_days(data : list[dict]) -> list[float]:
    pass

class Month(md):
    pass

def predict_by_months(data : list[Month]) -> list[float]:
    return mp(data)
