from sqlalchemy import Column, String, Integer, JSON

from pyrandseqbot.orm.connection import db


class ChatModel(db.base_model):
    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    chat_id = Column(String, unique=True, index=True, nullable=False)
    sequence = Column(JSON, nullable=True, default=None)
