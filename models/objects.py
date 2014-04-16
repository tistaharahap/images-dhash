from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
TABLES = {
    'hash': 'hashes'
}


class ImageHash(Base):
    __tablename__ = TABLES['hash']

    image_hash = Column(String(16), primary_key=True)
    image_filename = Column(String(255))
    image_created = Column(DateTime)

    active = Column(Integer)

    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            if hasattr(self, name):
                setattr(self, name, value)
            else:
                raise ValueError('Trying to set a non-existent attribute')

    def __repr__(self):
        return '%s: %s' % (self.image_filename, self.image_hash)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}