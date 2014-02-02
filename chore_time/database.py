from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = None

class Family(Base):
    __tablename__ = 'family'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)


    def __init__(self, name, email):
        pass


    def __eq__(self, other):
        try:
            return self.name == other.name and self.email == other.email
        except NameError:
            return False


def init_db(path_to_db):
    ''' Initialie a SQLite database at the location provided as path_to_db.'''
    global engine
    
    engine = create_engine(path_to_db)
    Base.metadata.create_all(engine)

    return engine 


def create_family(name, email):
    ''' Create a new Family. '''

    family = Family(name, email)
    session = sessionmaker(bind=engine)()
    session.add(family)
    session.commit()
