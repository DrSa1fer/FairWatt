from PIL.ExifTags import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .schemes.__base__ import Base

from .schemes import tariff_kind
from .schemes import facility_kind
from .schemes import settlement_kind
from .schemes import verified_grade
from .schemes import client
from .schemes import tariff
from .schemes import meter
from .schemes import daily_consumption
from .schemes import monthly_consumption
from .schemes import trip
from .schemes import facility
from .schemes import verified
from .schemes import trip_facility

__session : Session | None = None

def init(con_string : str) -> None:
    global __session
    engine  = create_engine(con_string)
    Base.metadata.create_all(engine)
    __session = Session(engine)

def free():
    global __session
    if __session is None:
        raise RuntimeError("DB session is not init")
    __session.close()
    __session = None

def session():
    global __session
    if __session is None:
        raise RuntimeError("DB session is not init")
    return __session
