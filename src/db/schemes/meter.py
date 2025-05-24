import sqlalchemy
from sqlalchemy import Sequence
from sqlalchemy.orm import relationship, mapped_column

from .__base__ import Base


class Meter(Base):
    __tablename__ = 'Meter'

    MeterID = sqlalchemy.Column(sqlalchemy.Integer, Sequence("meter_seq"), primary_key=True)

    FacilityID = mapped_column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Facility.FacilityID"))
    TariffID = mapped_column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Tariff.TariffID"))
    ClientID = mapped_column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Client.ClientID"))

    Facility = relationship('Facility')
    Tariff = relationship('Tariff')
    Client = relationship('Client')

