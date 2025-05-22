import sqlalchemy
from sqlalchemy import Sequence

from src.db.session import SqlAlchemyBase


class Client(SqlAlchemyBase):
    __tablename__ = 'Client'

    ClientID = sqlalchemy.Column(sqlalchemy.Integer, Sequence("client_seq"), primary_key=True)
    LastName = sqlalchemy.Column(sqlalchemy.String(length=25), nullable=False)
    FirstName = sqlalchemy.Column(sqlalchemy.String(length=25), nullable=False)
    FatherName = sqlalchemy.Column(sqlalchemy.String(length=25), nullable=False)
    Rating = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
