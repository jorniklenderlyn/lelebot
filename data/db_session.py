import sqlalchemy
import sqlalchemy.orm as orm
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()

__factory = None


USER = 'root'
PASSWORD = '101101011101password'


def create_db(db_file):
    engine = sqlalchemy.create_engine(f'mysql+mysqlconnector://{USER}:{PASSWORD}@localhost') # connect to server
    engine.execute(f"CREATE DATABASE {db_file.strip()}") #create db


def delete_db(db_file):
    engine = sqlalchemy.create_engine(f'mysql+mysqlconnector://{USER}:{PASSWORD}@localhost') # connect to server
    engine.execute(f"DROP DATABASE {db_file.strip()}") #create db


def global_init(db_file):
    global __factory

    if __factory:
        return

    try:
        e = create_engine(f"sqlite:///{db_file.strip()}?check_same_thread=False", echo=False)
    except:
        create_db('kcodbforbots')
        e = create_engine(f"sqlite:///{db_file.strip()}?check_same_thread=False", echo=False)
    __factory = orm.sessionmaker(bind=e)
    from . import __all_models

    SqlAlchemyBase.metadata.create_all(e)


def create_session() -> Session:
    global __factory
    return __factory()