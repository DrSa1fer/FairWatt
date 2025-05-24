from sqlalchemy import Integer, String
from sqlalchemy import Sequence
from sqlalchemy.orm import mapped_column, Mapped

from .__base__ import Base


class TariffKind(Base):
    __tablename__ = 'TariffKind'

    TariffKindID    = mapped_column(Integer, Sequence("tariffKind_seq"), primary_key=True)
    Name            = mapped_column(String(length=25), nullable=False)
