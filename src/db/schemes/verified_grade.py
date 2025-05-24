from sqlalchemy import Integer, String
from sqlalchemy import Sequence
from sqlalchemy.orm import mapped_column

from .__base__ import Base


class VerifiedGrade(Base):
    __tablename__ = 'VerifiedGrade'

    VerifiedGradeID = mapped_column(Integer, Sequence("verifiedGrade_seq"), primary_key=True)
    Name            = mapped_column(String(length=25), nullable=False)
