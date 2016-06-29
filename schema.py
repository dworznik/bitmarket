import os
import sys
from decimal import *
from sqlalchemy import Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from config import db_url

# import warnings
# from sqlalchemy.exc import SAWarning
# warnings.filterwarnings('ignore',
#  r"^Dialect sqlite\+pysqlite does \*not\* support Decimal objects natively\, "
#  "and SQLAlchemy must convert from floating point - rounding errors and other "
#  "issues may occur\. Please consider storing Decimal numbers as strings or "
#  "integers on this platform for lossless storage\..*",
#  SAWarning, r'^sqlalchemy\.sql\.type_api$')

Base = declarative_base()

class Swap(Base):
    __tablename__ = 'swap'
    id = Column(Integer, primary_key=True)
    swap_id = Column(Integer, nullable = False)
    amount = Column(Numeric)
    rate = Column(Numeric)
    earnings = Column(Numeric)
    timestamp = Column(Integer)
    error = Column(String)
    op = Column(String(20), nullable=False)

    @classmethod
    def fromjson(cls, json):
      return cls(swap_id = json['id'], amount = Decimal(str(json['amount'])),
        rate = Decimal(str(json['rate'])), earnings = Decimal(str(json['earnings'])), timestamp = json['timestamp'])

    def __repr__(self):
      return "<id: {id}, swap_id: {swap_id}, amount: {amount}, rate: {rate}, earnings: {earnings}, timestamp: {timestamp}>".format(
        id = self.id, swap_id = self.swap_id, amount = self.amount, rate = self.rate, earnings = self.earnings, timestamp = self.timestamp)


class Balance(Base):
  __tablename__ = 'balance'
  id = Column(Integer, primary_key=True)
  timestamp = Column(Integer)
  PPC_available = Column(Numeric)
  LiteMineX_available = Column(Numeric)
  DOGE_available = Column(Numeric)
  LTC_available = Column(Numeric)
  BTC_available = Column(Numeric)
  PLN_available = Column(Numeric)
  EUR_available = Column(Numeric)
  LTC_blocked = Column(Numeric)
  BTC_blocked = Column(Numeric)
  PLN_blocked = Column(Numeric)
  EUR_blocked = Column(Numeric)

engine = create_engine(db_url)
Base.metadata.create_all(engine)