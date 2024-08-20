import datetime

from sqlalchemy import Column, String, DateTime, Integer

from backend.database import Base


class Todo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    created = Column(DateTime, default=datetime.datetime.utcnow)


class ItemConfig(Base):
    __tablename__ = "item_config"

    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime, default=datetime.datetime.utcnow)

    # triangle size and color
    triangle_size = Column(Integer)
    triangle_color = Column(String)

    # circle size and color
    circle_size = Column(Integer)
    circle_color = Column(String)

    time_visible_ms = Column(Integer)
