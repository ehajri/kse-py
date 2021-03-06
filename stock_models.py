from peewee import *

database = MySQLDatabase('stock', **{'host': '127.0.0.1', 'port': 6033, 'user': 'root', 'password': 'passwd'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

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
    ask = IntegerField(null=True)
    ask_qty = IntegerField(null=True)
    bid = IntegerField(null=True)
    bid_qty = IntegerField(null=True)
    createdon = DateField()
    price = DecimalField()
    ticker = IntegerField(db_column='ticker_id')
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

