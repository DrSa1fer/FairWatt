import sqlalchemy
from sqlalchemy import Sequence
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase


class Facility(SqlAlchemyBase):
    __tablename__ = 'Facility'

    FacilityID = sqlalchemy.Column(sqlalchemy.Integer, Sequence("facility_seq"), primary_key=True)

    FacilityKindID = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("FacilityKind.FacilityKindID"))
    FacilityKind = relationship('FacilityKind')

    SettlementKindID = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("SettlementKind.SettlementKindID"))
    SettlementKind = relationship('SettlementKind')

    Square = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    hasElectricHeating = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False)
    hasElectricStove = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False)
    Address = sqlalchemy.Column(sqlalchemy.String(length=50), nullable=False)

    RegionID = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Region.RegionID"))
    Region = relationship('Region')
