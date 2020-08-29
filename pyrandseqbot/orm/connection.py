import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

_logger = logging.getLogger(__name__)


class Database:
    def __init__(self):
        self.base_model = declarative_base()
        self.create_session = None
        self.connected = False

    def connect(self, connection_string: str):
        engine = create_engine(
            connection_string,
            connect_args={'check_same_thread': False}
        )
        self.create_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        self.base_model.metadata.create_all(bind=engine)
        self.connected = True
        _logger.info('Database connection successfully established')


db = Database()
