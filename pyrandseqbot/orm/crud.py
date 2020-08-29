import logging
from typing import List

from sqlalchemy import asc
from sqlalchemy.orm import Session

from pyrandseqbot.orm import connection, models

_logger = logging.getLogger(__name__)


class BaseCrud:
    def __init__(self, base_model: connection.db.base_model, session: Session = None):
        self.bm = base_model
        if not session:
            session = connection.db.create_session()
        self.session = session

    def __del__(self):
        self.session.invalidate()

    def create(self, *args, **kwargs):
        return self.update(self.bm(*args, **kwargs))

    def read(self, **kwargs) -> connection.db.base_model:
        try:
            return self.query(**kwargs).first()
        except Exception as e:
            _logger.error(e)
            return None

    def read_all(self, skip: int = 0, limit: int = None, **kwargs) -> List[connection.db.base_model]:
        try:
            return self.query(**kwargs).offset(skip).limit(limit).all()
        except Exception as e:
            _logger.error(e)
            return []

    def update(self, data: connection.db.base_model) -> connection.db.base_model:
        try:
            self.session.add(data)
            self.session.commit()
            self.session.refresh(data)
        except Exception as e:
            _logger.error(e)
            self.session.rollback()
        return data

    def delete(self, data: connection.db.base_model) -> None:
        try:
            self.session.delete(data)
            self.session.commit()
        except Exception as e:
            _logger.error(e)
            self.session.rollback()

    def query(self, sort_by: str = 'id', **kwargs):
        try:
            return self.session.query(self.bm).filter(*(getattr(self.bm, k) == v for k, v in kwargs.items())).order_by(
                asc(getattr(self.bm, sort_by)))
        except Exception as e:
            _logger.error(e)
            return None

    def count(self):
        return self.session.query(self.bm.id).count()


class ChatCrud(BaseCrud):
    def __init__(self, **kwargs):
        super().__init__(base_model=models.ChatModel, **kwargs)
