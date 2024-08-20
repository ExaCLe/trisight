import datetime

from sqlalchemy import Column, String, DateTime, Integer

from backend.database import Base


class Todo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    created = Column(DateTime, default=datetime.datetime.utcnow)



