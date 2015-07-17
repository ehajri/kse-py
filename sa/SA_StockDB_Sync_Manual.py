from mubasher import *
from stock import *
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.sql import select
from datetime import date

mydatevar = date(2015, 7, 12)

def sync(Model, source, func, columns):
    # for RQuotes .order_by(-Model.id).limit(7000) (75000+) 11/07/2015
    a = source.execute(select([Model]).where(Model.timestamp>=mydatevar)).fetchall()
    toinsert = []
    count = 0
    print('Start!')
    for i in a:
        count += 1

        e = exists()
        for c in columns:
            e = e.where(getattr(Model, c)==getattr(i, c))
            
        (ret, ), = Session.query(e)
        if not ret:
            toinsert.append(i)
        
        if count % 1000 == 0:
            print('Processed %d' % count)
    
    print('to insert %d' % len(toinsert))

    # Reverse insert order
    # while toinsert:
    #     i = toinsert.pop()
    #     ins = func(Model, i)
    #     Session.execute(ins)

    for i in toinsert:
        ins = func(Model, i)
        Session.execute(ins)

# to insert RQuote
def toinsertfunc1(Model, i):
    ins = insert(Model).values(ticker_id=i.ticker_id, last=i.last, change=i.change, open=i.open, high=i.high, low=i.low, vol=i.vol, trade=i.trade, value=i.value, prev=i.prev, ref=i.ref, prev_date=i.prev_date, bid=i.bid, ask=i.ask, timestamp=i.timestamp)
    return ins

# to insert OBook
def toinsertfunc2(Model, i):
    ins = insert(Model).values(ticker_id=i.ticker_id, price=i.price, bid=i.bid, bid_qty=i.bid_qty, ask=i.ask, ask_qty=i.ask_qty, createdon=i.createdon, timestamp=i.timestamp)
    return ins

# to insert TimeSale
def toinsertfunc3(Model, i):
    ins = insert(Model).values(ticker_id=i.ticker_id, price=i.price, quantity=i.quantity, datetime=i.datetime, timestamp=i.timestamp)
    return ins

# to insert News
def toinsertfunc4(Model, i):
    ins = insert(Model).values(newsid=i.newsid, headline=i.headline, message=i.message, date=i.date, timestamp=i.timestamp)
    return ins

engine1 = create_engine('mysql://root:@localhost/stock')
imac = engine1.connect()

engine2 = create_engine('mysql://dev:youcanseeme@192.168.0.130/stock')
mbp = engine2.connect()

Session = scoped_session(sessionmaker(bind=engine2))

#sync(RQuote, mbp, toinsertfunc1, ['ticker_id', 'last', 'change', 'open', 'high', 'low', 'vol', 'trade', 'value', 'prev', 'ref', 'prev_date', 'bid', 'ask'])
#sync(OBook, mbp, toinsertfunc2, ['ticker_id', 'price', 'bid', 'bid_qty', 'ask', 'ask_qty', 'createdon'])
#sync(TimeSale, mbp, toinsertfunc3, ['ticker_id', 'price', 'quantity', 'datetime'])
#sync(News, mbp, toinsertfunc4, ['newsid', 'headline', 'message', 'date'])

sync(RQuote, imac, toinsertfunc1, ['ticker_id', 'last', 'change', 'open', 'high', 'low', 'vol', 'trade', 'value', 'prev', 'ref', 'prev_date', 'bid', 'ask'])
sync(OBook, imac, toinsertfunc2, ['ticker_id', 'price', 'bid', 'bid_qty', 'ask', 'ask_qty', 'createdon'])
sync(TimeSale, imac, toinsertfunc3, ['ticker_id', 'price', 'quantity', 'datetime'])
sync(News, imac, toinsertfunc4, ['newsid', 'headline', 'message', 'date'])
