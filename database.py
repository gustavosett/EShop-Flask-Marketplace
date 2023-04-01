from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
import contextlib


# Address
SQL_DATABASE_ALCHEMY_URL = 'sqlite:///./final_project_database.db'


# Connection
engine = create_engine(SQL_DATABASE_ALCHEMY_URL, connect_args={
                           # this argument is needed only for SQLite:
                           'check_same_thread': False })
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()

@contextlib.contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()