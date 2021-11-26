from typing import Optional

from sqlmodel import Field, SQLModel


class Chat(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    chat_id: str = Field(index=True, nullable=False)
    sequence: str = Field(index=False, nullable=True, default=None)
