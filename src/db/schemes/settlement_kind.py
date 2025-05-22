import sqlalchemy
from sqlalchemy import Sequence

from .db_session import SqlAlchemyBase


class SettlementKind(SqlAlchemyBase):
    __tablename__ = 'SettlementKind'

    SettlementKindID = sqlalchemy.Column(sqlalchemy.Integer, Sequence("settlementKind_seq"), primary_key=True)
    Name = sqlalchemy.Column(sqlalchemy.String(length=50), nullable=False)
    Addition = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
