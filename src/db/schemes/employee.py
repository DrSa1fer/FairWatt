from sqlalchemy import Integer, Float, String, BigInteger
from sqlalchemy import Sequence
from sqlalchemy.orm import mapped_column

from .__base__ import Base


class Employee(Base):
    __tablename__ = 'Employee'

    EmployeeID    = mapped_column(Integer, Sequence("employee_seq"), primary_key=True)
    LastName      = mapped_column(String(length=25), nullable=False)
    FirstName     = mapped_column(String(length=25), nullable=False)
    FatherName    = mapped_column(String(length=25), nullable=False)
