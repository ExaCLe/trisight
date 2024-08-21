import datetime
from typing import List, Optional

from sqlalchemy import String, DateTime, Integer, CheckConstraint, Boolean, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column


# Base class for the ORM models
class Base(DeclarativeBase):
    pass


class ItemConfig(Base):
    __tablename__ = "item_config"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)

    # triangle size and color
    triangle_size: Mapped[int] = mapped_column(Integer, CheckConstraint("triangle_size > 0"))
    triangle_color: Mapped[str] = mapped_column(String)

    # circle size and color
    circle_size: Mapped[int] = mapped_column(Integer, CheckConstraint("circle_size > 0"))
    circle_color: Mapped[str] = mapped_column(String)

    time_visible_ms: Mapped[int] = mapped_column(Integer, CheckConstraint("time_visible_ms > 0"))
    orientation: Mapped[str] = mapped_column(String, CheckConstraint("orientation IN ('N', 'E', 'S', 'W')"))

    # Relationship with ItemConfigResult
    item_config_results: Mapped[List["ItemConfigResult"]] = relationship(back_populates="item_config")


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)

    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)

    # Relationship with ItemConfigResult
    item_config_results: Mapped[List["ItemConfigResult"]] = relationship(back_populates="user")


class ItemConfigResult(Base):
    __tablename__ = "item_config_result"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)

    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"), nullable=True)
    item_config_id: Mapped[int] = mapped_column(ForeignKey("item_config.id"))
    correct: Mapped[bool] = mapped_column(Boolean)
    reaction_time_ms: Mapped[int] = mapped_column(Integer)
    response: Mapped[str] = mapped_column(String, CheckConstraint("response IN ('N', 'E', 'S', 'W')"))

    # Relationships
    item_config: Mapped["ItemConfig"] = relationship(back_populates="item_config_results")
    user: Mapped[Optional["User"]] = relationship(back_populates="item_config_results")
