from sqlalchemy import Date, Integer, ForeignKey, ARRAY, Float
from sqlalchemy.orm import relationship, mapped_column

from .__base__ import Base


class MonthlyConsumption(Base):
    __tablename__ = 'MonthlyConsumption'

    MeterID = mapped_column(Integer, ForeignKey("Meter.MeterID"), primary_key=True)

    Meter = relationship('Meter')
    Date = mapped_column(Date, primary_key=True)
    Data = mapped_column(ARRAY(Float))
