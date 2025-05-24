from sqlalchemy import Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy import Sequence
from sqlalchemy.orm import relationship, mapped_column

from .__base__ import Base


class Trip(Base):
    __tablename__ = 'Trip'

    TripID              = mapped_column(Integer, Sequence("trip_seq"), primary_key=True)
    FirstName           = mapped_column(String(length=25))
    LastName            = mapped_column(String(length=25))
    FromTime            = mapped_column(DateTime, nullable=False)
    ToTime              = mapped_column(DateTime, nullable=False)
