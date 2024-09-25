import datetime
from typing import List, Optional

from sqlalchemy import (
    String,
    DateTime,
    Integer,
    CheckConstraint,
    Boolean,
    ForeignKey,
    Table,
    Column,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column

from backend.database import Base


# Association table for the many-to-many relationship between TestConfig and ItemConfig
test_config_item_config_association = Table(
    "test_config_item_config",
    Base.metadata,
    Column("test_config_id", ForeignKey("test_config.id"), primary_key=True),
    Column("item_config_id", ForeignKey("item_config.id"), primary_key=True),
)

# Association table for the many-to-many relationship between TestConfigResult and ItemConfigResult
test_config_result_item_config_result_association = Table(
    "test_config_result_item_config_result",
    Base.metadata,
    Column(
        "test_config_result_id", ForeignKey("test_config_result.id"), primary_key=True
    ),
    Column(
        "item_config_result_id", ForeignKey("item_config_result.id"), primary_key=True
    ),
)


class ItemConfig(Base):
    __tablename__ = "item_config"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )

    # triangle size and color
    triangle_size: Mapped[int] = mapped_column(
        Integer, CheckConstraint("triangle_size > 0")
    )
    triangle_color: Mapped[str] = mapped_column(String)

    # circle size and color
    circle_size: Mapped[int] = mapped_column(
        Integer, CheckConstraint("circle_size > 0")
    )
    circle_color: Mapped[str] = mapped_column(String)

    time_visible_ms: Mapped[int] = mapped_column(
        Integer, CheckConstraint("time_visible_ms > 0")
    )
    orientation: Mapped[str] = mapped_column(
        String, CheckConstraint("orientation IN ('N', 'E', 'S', 'W')")
    )

    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"), nullable=True)

    # Relationship with ItemConfigResult
    item_config_results: Mapped[List["ItemConfigResult"]] = relationship(
        back_populates="item_config"
    )

    # Relationship with User
    user: Mapped[Optional["User"]] = relationship(back_populates="item_configs")

    # Many-to-many relationship with TestConfig
    test_configs: Mapped[List["TestConfig"]] = relationship(
        secondary=test_config_item_config_association, back_populates="item_configs"
    )


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )

    username: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    hashed_password: Mapped[str] = mapped_column(String)

    issued_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=True
    )  # for the logout feature

    # Relationship with ItemConfigResult
    item_config_results: Mapped[List["ItemConfigResult"]] = relationship(
        back_populates="user"
    )

    # Relationship with ItemConfig
    item_configs: Mapped[List["ItemConfig"]] = relationship(back_populates="user")

    # Relationship with TestConfig and TestConfigResult
    test_configs: Mapped[List["TestConfig"]] = relationship(back_populates="user")
    test_config_results: Mapped[List["TestConfigResult"]] = relationship(
        back_populates="user"
    )


class ItemConfigResult(Base):
    __tablename__ = "item_config_result"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )

    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"), nullable=True)
    item_config_id: Mapped[int] = mapped_column(ForeignKey("item_config.id"))
    correct: Mapped[bool] = mapped_column(Boolean)
    reaction_time_ms: Mapped[int] = mapped_column(Integer)
    response: Mapped[str] = mapped_column(
        String, CheckConstraint("response IN ('N', 'E', 'S', 'W')")
    )

    # Relationships
    item_config: Mapped["ItemConfig"] = relationship(
        back_populates="item_config_results"
    )
    user: Mapped[Optional["User"]] = relationship(back_populates="item_config_results")

    # Many-to-many relationship with TestConfigResult
    test_config_results: Mapped[List["TestConfigResult"]] = relationship(
        secondary=test_config_result_item_config_result_association,
        back_populates="item_config_results",
    )


class TestConfig(Base):
    __tablename__ = "test_config"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )

    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"), nullable=True)
    name: Mapped[str] = mapped_column(String)

    # Many-to-many relationship with ItemConfig
    item_configs: Mapped[List["ItemConfig"]] = relationship(
        secondary=test_config_item_config_association, back_populates="test_configs"
    )

    # Relationship with User
    user: Mapped[Optional["User"]] = relationship(back_populates="test_configs")

    # Relationship with TestConfigResult
    test_config_results: Mapped[List["TestConfigResult"]] = relationship(
        back_populates="test_config"
    )


class TestConfigResult(Base):
    __tablename__ = "test_config_result"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )

    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"), nullable=True)
    test_config_id: Mapped[int] = mapped_column(
        ForeignKey("test_config.id"), nullable=False
    )
    time: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )
    correct_answers: Mapped[int] = mapped_column(Integer)
    wrong_answers: Mapped[int] = mapped_column(Integer)

    # Many-to-many relationship with ItemConfigResult
    item_config_results: Mapped[List["ItemConfigResult"]] = relationship(
        secondary=test_config_result_item_config_result_association,
        back_populates="test_config_results",
    )

    # Relationship with User
    user: Mapped["User"] = relationship(back_populates="test_config_results")

    # Relationship with TestConfig
    test_config: Mapped["TestConfig"] = relationship(
        back_populates="test_config_results"
    )
