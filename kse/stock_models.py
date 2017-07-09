from peewee import *
import os


# database = MySQLDatabase('stock', **{'host': os.environ['MYSQL_PORT_3306_TCP_ADDR'],
#                          'port': 3306, 'user': 'root', 'password': os.environ['MYSQL_ENV_MYSQL_ROOT_PASSWORD']})

db = MySQLDatabase('stock', **{'user': 'root'})

class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = db


class News(BaseModel):
    date = DateTimeField()
    headline = CharField()
    message = TextField()
    newsid = IntegerField()
    timestamp = DateTimeField()

    class Meta:
        db_table = 'News'
        indexes = (
            (('newsid', 'headline', 'date'), True),
        )


class Obook(BaseModel):
    ask = TextField()
    ask_qty = TextField()
    bid = TextField()
    bid_qty = TextField()
    createdon = DateField()
    price = TextField()
    ticker = TextField(db_column='ticker_id')
    timestamp = DateTimeField()

    class Meta:
        db_table = 'OBook'
        indexes = (
            (('ticker', 'price', 'bid', 'bid_qty', 'ask', 'ask_qty', 'createdon'), True),
        )

class Rquotes(BaseModel):
    ask = DecimalField(null=True)
    bid = DecimalField(null=True)
    change = DecimalField()
    high = DecimalField(null=True)
    last = DecimalField(null=True)
    low = DecimalField(null=True)
    open = DecimalField(null=True)
    prev = DecimalField()
    prev_date = DateField()
    ref = DecimalField()
    ticker = IntegerField(db_column='ticker_id')
    timestamp = DateTimeField()
    trade = IntegerField()
    value = DecimalField(null=True)
    vol = IntegerField(null=True)

    class Meta:
        db_table = 'RQuotes'
        indexes = (
            (('ticker', 'last', 'change', 'open', 'high', 'low', 'vol', 'trade', 'value', 'prev', 'ref', 'prev_date', 'bid', 'ask'), True),
            (('ticker', 'timestamp'), True),
        )


class Tickers(BaseModel):
    ticker = IntegerField(db_column='ticker_id')

    class Meta:
        db_table = 'Tickers'


class Timesale(BaseModel):
    datetime = DateTimeField()
    price = DecimalField()
    quantity = IntegerField()
    ticker = IntegerField(db_column='ticker_id')
    timestamp = DateTimeField()

    class Meta:
        db_table = 'TimeSale'
        indexes = (
            (('ticker', 'datetime'), False),
            (('ticker', 'price', 'quantity', 'datetime'), True),
        )


class Running(BaseModel):
    funcname = CharField()
    lastrun = DateTimeField()

    class Meta:
        db_table = 'running'


class test(BaseModel):
    field1 = IntegerField(null=True)
    field2 = IntegerField(null=True)

    class Meta:
        db_table = 'test'
        indexes = (
            (('field1', 'field2'), True),
        )