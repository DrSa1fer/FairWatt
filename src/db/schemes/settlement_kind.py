from sqlalchemy import Integer, String
from sqlalchemy import Sequence
from sqlalchemy.orm import mapped_column

from .__base__ import Base


class SettlementKind(Base):
    __tablename__ = 'SettlementKind'

    SettlementKindID    = mapped_column(Integer, Sequence("settlementKind_seq"), primary_key=True)
    Name                = mapped_column(String(length=50), nullable=False)
