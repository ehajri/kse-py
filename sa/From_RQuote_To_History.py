from mubasher import *
from stock import *
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.sql import select




stock_engine = create_engine('mysql://root:@localhost/stock')
mubasher_engine = create_engine('mysql://root:@localhost/mubasher')

Session_S = scoped_session(sessionmaker(bind=stock_engine))
Session_M = scoped_session(sessionmaker(bind=mubasher_engine))

tt = t_rquotes_summary.c
q = Session_S.query(t_rquotes_summary).filter(tt.datetime >= '2015-07-15')
q = q.filter(and_(tt.open != 0, tt.high != 0, tt.low != 0, tt.closing != 0, tt.volume != 0))

for i in q:
    ins = insert(History).values(stock=i.stock, datetime=i.datetime, open=i.open, high=i.high, low=i.low, closing=i.closing, volume=i.volume, companies=i.companies)
    Session_M.execute(ins)
