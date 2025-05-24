from sqlalchemy import Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy import Sequence
from sqlalchemy.orm import relationship, mapped_column

from .__base__ import Base


class Trip(Base):
    __tablename__ = 'Trip'

    EmployeeID          = mapped_column(Integer, ForeignKey("Employee.EmployeeID"))

    TripID              = mapped_column(Integer, Sequence("trip_seq"), primary_key=True)
    Employee            = relationship("Employee")
    FromTime            = mapped_column(DateTime, nullable=False)
    ToTime              = mapped_column(DateTime, nullable=False)
