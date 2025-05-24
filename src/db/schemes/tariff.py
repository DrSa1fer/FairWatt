from sqlalchemy import Integer, Float, ForeignKey
from sqlalchemy import Sequence
from sqlalchemy.orm import relationship, mapped_column

from .__base__ import Base


class Tariff(Base):
    __tablename__ = 'Tariff'

    TariffKindID    = mapped_column(Integer, ForeignKey("TariffKind.TariffKindID"))

    TariffID        = mapped_column(Integer, Sequence("tariff_seq"), primary_key=True)
    TariffKind      = relationship('TariffKind')
    Standard        = mapped_column(Float, nullable=False)
    Price           = mapped_column(Float, nullable=False)
