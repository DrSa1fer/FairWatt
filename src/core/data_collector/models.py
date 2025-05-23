from pydantic import BaseModel
from typing import Literal

TYPE_ = Literal["branch",
    "building",
    "street",
    "parking",
    "station",
    "station_entrance",
    "station_platform",
    "attraction",
    "crossroad",
    "gate",
    "road",
    "route",
    "adm_div",
]

class TwoGis(BaseModel):
    type_ : TYPE_
    purpose_name: str
