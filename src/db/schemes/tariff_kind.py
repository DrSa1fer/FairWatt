import sqlalchemy
from sqlalchemy import Sequence

from src.db.session import SqlAlchemyBase


class TariffKind(SqlAlchemyBase):
    __tablename__ = 'TariffKind'

    TariffKindID = sqlalchemy.Column(sqlalchemy.Integer, Sequence("tariffKind_seq"), primary_key=True)
    Name = sqlalchemy.Column(sqlalchemy.String(length=25), nullable=False)
