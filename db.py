from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from config import db_url
from schema import Balance, Base, Swap

engine = create_engine(db_url)
Base.metadata.bind = engine

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


