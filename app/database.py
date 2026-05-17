import sqlalchemy
import sqlalchemy.orm as orm
from .models import SqlAlchemyBase

__factory = None


def global_init(db_file):
    global __factory
    if __factory:
        return

    conn = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    engine = sqlalchemy.create_engine(conn, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    SqlAlchemyBase.metadata.create_all(engine)


def create_session():
    global __factory
    return __factory()