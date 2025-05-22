import sqlalchemy
from sqlalchemy.orm import relationship

from src.db.session import SqlAlchemyBase


class Consumption(SqlAlchemyBase):
    __tablename__ = 'Consumption'

    MeterID = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Meter.MeterID"), primary_key=True)
    Meter = relationship('Meter')
    Date = sqlalchemy.Column(sqlalchemy.Date, primary_key=True)
    Data = sqlalchemy.Column(sqlalchemy.JSON)
