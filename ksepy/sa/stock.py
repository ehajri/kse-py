# coding: utf-8
from sqlalchemy import BigInteger, Column, Date, DateTime, Index, Integer, Numeric, String, Table, Text, text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class News(Base):
    __tablename__ = 'News'
    __table_args__ = (
        Index('newsid', 'newsid', 'headline', 'date', unique=True),
    )

    id = Column(Integer, primary_key=True)
    newsid = Column(Integer, nullable=False)
    headline = Column(String(255), nullable=False, server_default=text("''"))
    message = Column(Text, nullable=False)
    date = Column(DateTime, nullable=False)
    timestamp = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))


class NewsOld(Base):
    __tablename__ = 'NewsOld'

    id = Column(Integer, primary_key=True)
    headline = Column(String(255, 'utf8_unicode_ci'))
    url = Column(String(255))
    date = Column(DateTime)
    timestamp = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))


class OBook(Base):
    __tablename__ = 'OBook'
    __table_args__ = (
        Index('idx_obook_uniquerecord', 'ticker_id', 'price', 'bid', 'bid_qty', 'ask', 'ask_qty', 'createdon', unique=True),
    )

    id = Column(Integer, primary_key=True)
    ticker_id = Column(Integer, nullable=False)
    price = Column(Numeric(12, 3), nullable=False)
    bid = Column(Integer)
    bid_qty = Column(Integer)
    ask = Column(Integer)
    ask_qty = Column(Integer)
    createdon = Column(Date, nullable=False)
    timestamp = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))


class RQuote(Base):
    __tablename__ = 'RQuotes'
    __table_args__ = (
        Index('idx_rquotes_uniquerecord', 'ticker_id', 'last', 'change', 'open', 'high', 'low', 'vol', 'trade', 'value', 'prev', 'ref', 'prev_date', 'bid', 'ask', unique=True),
        Index('index_unique', 'ticker_id', 'timestamp', unique=True)
    )

    id = Column(Integer, primary_key=True)
    ticker_id = Column(Integer, nullable=False)
    last = Column(Numeric(12, 3))
    change = Column(Numeric(12, 3), nullable=False)
    open = Column(Numeric(12, 3))
    high = Column(Numeric(12, 3))
    low = Column(Numeric(12, 3))
    vol = Column(Integer)
    trade = Column(Integer, nullable=False)
    value = Column(Numeric(12, 3))
    prev = Column(Numeric(12, 3), nullable=False)
    ref = Column(Numeric(12, 3), nullable=False)
    prev_date = Column(Date, nullable=False)
    bid = Column(Numeric(12, 3))
    ask = Column(Numeric(12, 3))
    timestamp = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

# class RQuoteSummary(Base):
#     __tablename__ = 'rquotes_summary'
# 
#     id = Column(Integer, primary_key=True)
#     datetime = Column(DateTime, nullable=False)
#     stock = Column(String(20), nullable=False, server_default=text("''"))
#     open = Column(Numeric(16, 3), nullable=False)
#     high = Column(Numeric(16, 3), nullable=False)
#     low = Column(Numeric(16, 3), nullable=False)
#     closing = Column(Numeric(16, 3), nullable=False)
#     volume = Column(BigInteger, nullable=False)
#     companies = Column(Integer)
    

class Ticker(Base):
    __tablename__ = 'Tickers'

    id = Column(Integer, primary_key=True)
    ticker_id = Column(Integer, nullable=False)


class TimeSale(Base):
    __tablename__ = 'TimeSale'
    __table_args__ = (
        Index('idx_timesale_uniquerecord', 'ticker_id', 'price', 'quantity', 'datetime', unique=True),
    )

    id = Column(Integer, primary_key=True)
    ticker_id = Column(Integer, nullable=False)
    price = Column(Numeric(12, 3), nullable=False)
    quantity = Column(Integer, nullable=False)
    datetime = Column(DateTime, nullable=False)
    timestamp = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


t_requotes_presummary = Table(
    'requotes_presummary', metadata,
    Column('ts', DateTime),
    Column('mm', Integer),
    Column('dd', Integer),
    Column('ticker_id', Integer)
)


t_rquotes_summary = Table(
    'rquotes_summary', metadata,
    Column('id', Integer, server_default=text("'0'")),
    Column('datetime', Date),
    Column('stock', String(11)),
    Column('open', Numeric(12, 3)),
    Column('high', Numeric(12, 3)),
    Column('low', Numeric(12, 3)),
    Column('closing', Numeric(12, 3)),
    Column('volume', Integer),
    Column('companies', Integer, server_default=text("'0'"))
)


class Running(Base):
    __tablename__ = 'running'

    id = Column(Integer, primary_key=True)
    funcname = Column(String(255), nullable=False, server_default=text("''"))
    lastrun = Column(DateTime, nullable=False)
    
    def hello():
        print(funcname)

class Test(Base):
    __tablename__ = 'test'

    id = Column(Integer, primary_key=True)
    msg = Column(String(11), server_default=text("''"))
    dt = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))


t_testv = Table(
    'testv', metadata,
    Column('id', Integer, server_default=text("'0'")),
    Column('msg', String(11)),
    Column('dt', DateTime)
)
