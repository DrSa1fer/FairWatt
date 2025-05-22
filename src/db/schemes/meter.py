import sqlalchemy
from sqlalchemy import Sequence
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase


class Meter(SqlAlchemyBase):
    __tablename__ = 'Meter'

    MeterID = sqlalchemy.Column(sqlalchemy.Integer, Sequence("meter_seq"), primary_key=True)

    FacilityID = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Facility.FacilityID"))
    Facility = relationship('Facility')

    TariffID = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Tariff.TariffID"))
    Tariff = relationship('Tariff')

    ClientID = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Client.ClientID"))
    Client = relationship('Client')

