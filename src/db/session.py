import sqlalchemy as sa
import sqlalchemy.orm as  orm
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

SqlAlchemyBase = declarative_base()

__factory = None

def global_init(db_file):
    global __factory
    if __factory:
        return

    engine = sa.create_engine(db_file, echo=False)
    __factory = orm.sessionmaker(bind=engine)
    __factory.expire_on_commit = False
    from .schemes import __all_models
    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    return __factory()
