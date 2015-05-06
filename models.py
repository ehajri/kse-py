from peewee import *

def DB():
    return MySQLDatabase('stock2', host='localhost', user='dev', passwd='youcanseeme')

class Parent(Model):
    class Meta:
        database = DB()

class test(Parent):
    id          = PrimaryKeyField()
    msg         = CharField()
    dt          = DateTimeField()

class News(Parent):
    id          = PrimaryKeyField()
    newsid      = IntegerField()
    headline    = CharField()
    message     = CharField()
    date        = DateTimeField()
    timestamp   = DateTimeField()

class OBook(Parent):
    id          = PrimaryKeyField()
    ticker_id   = IntegerField()
    price       = DecimalField()
    bid         = IntegerField()
    bid_qty     = IntegerField()
    ask         = IntegerField()
    ask_qty     = IntegerField()
    timestamp   = DateTimeField()

class Tickers(Parent):
    id          = PrimaryKeyField()
    ticker_id   = IntegerField()

class TimeSale(Parent):
    id          = PrimaryKeyField()
    ticker_id   = IntegerField()
    price       = DecimalField()
    quantity    = IntegerField()
    datetime    = DateTimeField()
    timestamp   = DateTimeField()

class RQuotes(Parent):
    id          = PrimaryKeyField()
    ticker_id   = IntegerField()
    last        = DecimalField()
    change      = DecimalField()
    open        = DecimalField()
    high        = DecimalField()
    low         = DecimalField()
    vol         = IntegerField()
    trade       = IntegerField()
    value       = DecimalField()
    prev        = DecimalField()
    ref         = DecimalField()
    prev_date   = DateField()
    bid         = DecimalField()
    ask         = DecimalField()
    timestamp   = DateTimeField()

def BulkInsert(dict):
    with DB().atomic():
        for data_dict in dict:
            RQuotes.create(**data_dict)
