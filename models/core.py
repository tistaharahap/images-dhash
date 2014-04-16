from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.objects import *
from settings import get_db_settings
import time
import hashlib


class CoreModel(object):
    db = None

    def __init__(self):
        db_uri = get_db_settings('dev').uri

        self.db = create_engine(db_uri, convert_unicode=True)
        self.session = None

        self.get_session()

    def get_session(self):
        self.session = scoped_session(sessionmaker(autocommit=False,
                                                   autoflush=False,
                                                   bind=self.db))

        Base.query = self.session.query_property()
        Base.metadata.create_all(bind=self.db)

    @classmethod
    def md5(cls, s):
        m = hashlib.md5()
        m.update(s)
        return m.hexdigest()

    @classmethod
    def get_unix_time(cls):
        return int(time.time())