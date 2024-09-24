# database.py
from sqlalchemy import create_engine, MetaData, event, Engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.engine import Engine
from config import settings

DATABASE_URL = settings.DATABASE_URL

# Determine if the database is SQLite
IS_SQLITE = DATABASE_URL.startswith("sqlite")

# Set connect_args conditionally
if IS_SQLITE:
    connect_args = {"check_same_thread": False}
else:
    connect_args = {}

# Create the engine
engine = create_engine(DATABASE_URL, connect_args=connect_args)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()
metadata = MetaData()

# Enable foreign key support for SQLite
if IS_SQLITE:

    @event.listens_for(Engine, "connect")
    def enable_foreign_keys(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
