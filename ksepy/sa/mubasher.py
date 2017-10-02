# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Float, Index, Integer, Numeric, String, Text, text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()
metadata = Base.metadata


class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    stk = Column(Integer, nullable=False)
    ticker = Column(String(11), nullable=False, server_default=text("''"))
    name = Column(String(255), nullable=False, server_default=text("''"))
    sector = Column(String(20), nullable=False, server_default=text("''"))
    islamic = Column(Integer, nullable=False, server_default=text("'0'"))
    stocks = relationship('History', backref='Company')


class History(Base):
    __tablename__ = 'history'
    __table_args__ = (
        Index('stock', 'stock', 'datetime', 'open', 'high', 'low', 'closing', 'volume', unique=True),
    )

    id = Column(Integer, primary_key=True)
    stock = Column(String(20), nullable=False, server_default=text("''"))
    datetime = Column(DateTime, nullable=False)
    open = Column(Numeric(16, 3), nullable=False)
    high = Column(Numeric(16, 3), nullable=False)
    low = Column(Numeric(16, 3), nullable=False)
    closing = Column(Numeric(16, 3), nullable=False)
    volume = Column(BigInteger, nullable=False)
    createdon = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    companies = Column(Integer, ForeignKey('companies.id'))


class Json(Base):
    __tablename__ = 'jsons'
    __table_args__ = (
        Index('json', 'json', 'lang', 'uri'),
    )

    id = Column(Integer, primary_key=True)
    json = Column(Text, nullable=False)
    lang = Column(String(2), nullable=False, server_default=text("''"))
    uri = Column(String(100), nullable=False, server_default=text("''"))
    createdon = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))


class Stock(Base):
    __tablename__ = 'stocks'

    id = Column(Integer, primary_key=True)
    stock = Column(String(20))
    pb_ratio = Column(Numeric(20, 3))
    market_cap = Column(Numeric(20, 3))
    total_assets_growth_percentage = Column(Float(10))
    pe_ratio = Column(Numeric(11, 3))
    book_value = Column(Numeric(11, 3))
    eps = Column(Numeric(11, 3))
    par_value = Column(Numeric(16, 3))
    currency = Column(String(20))
    capital = Column(Numeric(20, 3))
    total_share = Column(BigInteger)
    createdon = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
