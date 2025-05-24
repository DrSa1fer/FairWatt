from sqlalchemy import Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy import Sequence
from sqlalchemy.orm import relationship, mapped_column

from .__base__ import Base


class Verified(Base):
    __tablename__ = 'Verified'

    FacilityID          = mapped_column(Integer, ForeignKey("Facility.FacilityID"))
    ClientID            = mapped_column(Integer, ForeignKey("Client.ClientID"))
    GradeID             = mapped_column(Integer, ForeignKey("VerifiedGrade.VerifiedGradeID"))
    TripID              = mapped_column(Integer, ForeignKey("Trip.TripID"))

    VerifiedID          = mapped_column(Integer, Sequence("verified_seq"), primary_key=True)
    Facility            = relationship("Facility")
    Client              = relationship("Client")
    Grade               = relationship("VerifiedGrade")
    Trip                = relationship("Trip")
    Time                = mapped_column(DateTime, nullable=False)
