from sqlalchemy import Integer, Float, String, BigInteger
from sqlalchemy import Sequence
from sqlalchemy.orm import mapped_column

from .__base__ import Base


class Client(Base):
    __tablename__ = 'Client'

    ClientID    = mapped_column(Integer, Sequence("client_seq"), primary_key=True)
    LastName    = mapped_column(String(length=25), nullable=False)
    FirstName   = mapped_column(String(length=25), nullable=False)
    FatherName  = mapped_column(String(length=25), nullable=False)
    Rating      = mapped_column(Float, nullable=False)
    Email       = mapped_column(String(length=25), unique=True, nullable=True)
    Phone       = mapped_column(BigInteger, unique=True)

