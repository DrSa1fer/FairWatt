from sqlalchemy import Integer, Column, ForeignKey, String, Boolean
from sqlalchemy import Sequence
from sqlalchemy.orm import relationship, mapped_column

from .__base__ import Base


class Meter(Base):
    __tablename__ = 'Meter'

    MeterID = Column(Integer, Sequence("meter_seq"), primary_key=True)

    FacilityID = mapped_column(Integer, ForeignKey("Facility.FacilityID"))
    TariffID = mapped_column(Integer, ForeignKey("Tariff.TariffID"))
    ClientID = mapped_column(Integer, ForeignKey("Client.ClientID"))

    Notes = mapped_column(String(length=255))
    Facility = relationship('Facility')
    Tariff = relationship('Tariff')
    Client = relationship('Client')
    IsIot = mapped_column(Boolean)

    DailyConsumptions = relationship("DailyConsumption", back_populates="Meter")
    MonthlyConsumptions = relationship("MonthlyConsumption", back_populates="Meter")

