from sqlalchemy import Integer, String, ForeignKey, Boolean, Float
from sqlalchemy import Sequence
from sqlalchemy.orm import relationship, mapped_column

from .__base__ import Base


class Facility(Base):
    __tablename__ = 'Facility'

    FacilityKindID      = mapped_column(Integer, ForeignKey("FacilityKind.FacilityKindID"))

    FacilityID          = mapped_column(Integer, Sequence("facility_seq"), primary_key=True)
    FacilityKind        = relationship('FacilityKind')
    Rooms               = mapped_column(Integer, nullable=True)
    Residents           = mapped_column(Integer, nullable=True)
    Square              = mapped_column(Integer, nullable=True)
    Address             = mapped_column(String(length=150), nullable=False)
    Longitude           = mapped_column(Float, nullable=True)
    Latitude            = mapped_column(Float, nullable=True)

    Meters = relationship("Meter", back_populates="facility")
