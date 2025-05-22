import sqlalchemy
from sqlalchemy import Sequence

from src.db.session import SqlAlchemyBase


class FacilityKind(SqlAlchemyBase):
    __tablename__ = 'FacilityKind'

    FacilityKindID = sqlalchemy.Column(sqlalchemy.Integer, Sequence("facilityKind_seq"), primary_key=True)
    Name = sqlalchemy.Column(sqlalchemy.String(length=50), nullable=False)
    Addition = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
