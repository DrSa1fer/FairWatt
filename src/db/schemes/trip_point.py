from sqlalchemy import Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy import Sequence
from sqlalchemy.orm import relationship, mapped_column

from .__base__ import Base


class TripPoint(Base):
    __tablename__ = 'TripPoint'

    TripID = mapped_column(Integer, ForeignKey("Trip.TripID"))
    FacilityID = mapped_column(Integer, ForeignKey("Facility.FacilityID"))

    TripPoint           = mapped_column(Integer, Sequence("tripPoint_seq"), primary_key=True)
    Trip                = relationship("Trip")
    Facility            = relationship("Facility")
    IsFirst             = mapped_column(Boolean, nullable=False)
