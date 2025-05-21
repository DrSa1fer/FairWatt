import sqlalchemy
from sqlalchemy import Sequence
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase


class Tariff(SqlAlchemyBase):
    __tablename__ = 'Tariff'

    TariffID = sqlalchemy.Column(sqlalchemy.Integer, Sequence("tariff_seq"), primary_key=True)
    TariffKindID = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("TariffKind.TariffKindID"))
    TariffKind = relationship('TariffKind')
    Standard = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    Price = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
