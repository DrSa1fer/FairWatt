from sqlalchemy import Date, Integer, ForeignKey, ARRAY, Float, Sequence
from sqlalchemy.orm import relationship, mapped_column

from .__base__ import Base


class DailyConsumption(Base):
    __tablename__ = 'DailyConsumption'

    MeterID = mapped_column(Integer, ForeignKey("Meter.MeterID"))

    DailyConsumptionID = mapped_column(Integer, Sequence("dailyConsumption_seq"), primary_key=True)
    Meter = relationship('Meter')
    Rating = mapped_column(Float, nullable=True)
    Date = mapped_column(Date)
    Data = mapped_column(ARRAY(Float))
