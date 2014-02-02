from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref

Base = declarative_base()
engine = None


class Family(Base):
    __tablename__ = 'family'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        try:
            return self.name == other.name and self.id == other.id
        except NameError:
            return False


class FamilyMember(Base):
    __tablename__ = 'family_member'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    family_id = Column(Integer, ForeignKey('family.id'))

    family = relationship("Family", backref=backref('members', order_by=id))

    def __init__(self, family_id, name, email):
        self.family_id = family_id
        self.name = name
        self.email = email

    def __eq__(self, other):
        try:
            return (self.id == other.id
                    and self.name == other.name
                    and self.email == other.email)
        except NameError:
            return False

    def __repr__(self):
        return "<FamilyMember {0} - {1} - {2}>".format(self.name,
                                                       self.email,
                                                       self.id)


def init_db(path_to_db):
    ''' Initialie a SQLite database at the location provided as path_to_db.'''
    global engine

    engine = create_engine(path_to_db)
    Base.metadata.create_all(engine)

    return engine


def create_family(name):
    ''' Create a new Family. '''

    family = Family(name)
    session = sessionmaker(bind=engine)()
    session.add(family)
    session.commit()
    return family


def create_family_member(family_id, name, email):
    ''' Create a member in the given family. If family_id does not exist,
    raise ValueError.

    '''

    session = sessionmaker(bind=engine)()
    family = session.query(Family).filter_by(id=family_id).first()
    if not family:
        raise ValueError('No family with id <{}>'.format(family_id))
    family_member = FamilyMember(family_id, name, email)
    session.add(family_member)
    session.commit()
