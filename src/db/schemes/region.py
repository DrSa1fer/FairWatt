import sqlalchemy
from sqlalchemy import Sequence

from src.db.session import SqlAlchemyBase


class Region(SqlAlchemyBase):
    __tablename__ = 'Region'

    RegionID = sqlalchemy.Column(sqlalchemy.Integer, Sequence("region_seq"), primary_key=True)
    Name = sqlalchemy.Column(sqlalchemy.String(length=50), nullable=False)
    Addition = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
