
from urllib.parse import quote
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from utilities.config_variables import MYSQL_DATABASE, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_USERNAME


SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{MYSQL_USERNAME}:{quote(MYSQL_PASSWORD, safe='')}@{MYSQL_HOST}/{MYSQL_DATABASE}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
