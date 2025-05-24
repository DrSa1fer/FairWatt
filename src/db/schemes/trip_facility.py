from sqlalchemy import Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy import Sequence
from sqlalchemy.orm import relationship, mapped_column

from .__base__ import Base


class TripFacility(Base):
    __tablename__ = 'TripFacility'

    TripID = mapped_column(Integer, ForeignKey("Trip.TripID"))
    FacilityID = mapped_column(Integer, ForeignKey("Facility.FacilityID"))

    TripFacilityID      = mapped_column(Integer, Sequence("tripFacility_seq"), primary_key=True)
    Trip                = relationship("Trip")
    Facility            = relationship("Facility")
