from sqlalchemy import Integer, String, ForeignKey, Boolean
from sqlalchemy import Sequence
from sqlalchemy.orm import relationship, mapped_column

from .__base__ import Base


class Facility(Base):
    __tablename__ = 'Facility'

    FacilityKindID      = mapped_column(Integer, ForeignKey("FacilityKind.FacilityKindID"))
    SettlementKindID    = mapped_column(Integer, ForeignKey("SettlementKind.SettlementKindID"))

    FacilityID          = mapped_column(Integer, Sequence("facility_seq"), primary_key=True)
    FacilityKind        = relationship('FacilityKind')
    SettlementKind      = relationship('SettlementKind')
    Square              = mapped_column(Integer, nullable=True)
    Address             = mapped_column(String(length=50), nullable=False)
