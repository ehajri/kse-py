from mubasher import *
from stock import *
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.sql import select    

def StockWithHighestVolume():
    s = (Session_M.query(History, func.sum(History.volume))
                 .filter(History.datetime>='2015-02-01')
                 .group_by(History.companies)
                 .order_by(func.sum(History.volume).desc())
                 .limit(10))
    s = s.all()

    print('%-8s%-15s%-15s' % ('islamic', 'stock', 'volume'))
    for i in s:
        if i[0].Company.islamic == 1:
            islamic = 'Yes'
        else:
            islamic = 'No'
        print('%-8s%-15s%-15s' % (islamic, i[0].stock, '{0:,g}'.format(i[1])))

def StockWithMostTelda():
    s = (Session_M.query(History, func.min(History.volume), func.max(History.volume), func.max(History.volume) - func.min(History.volume))
                 .filter(History.datetime>='2015-02-01')
                 .group_by(History.companies)
                 .order_by((func.max(History.volume) - func.min(History.volume)).desc())
                 .limit(10))
    s = s.all()

    print('%-8s%-15s%-15s%-15s%-15s' % ('islamic', 'stock', 'min', 'max', 'telda'))
    for i in s:
        if i[0].Company.islamic == 1:
            islamic = 'Yes'
        else:
            islamic = 'No'
        
        print('%-8s%-15s%-15s%-15s%-15s' % (islamic, i[0].stock, '{0:,d}'.format(i[1]), '{0:,d}'.format(i[2]), '{0:,d}'.format(i[3])))

def StockWithMostTrades():
    s = (Session_M.query(History, func.min(History.volume), func.max(History.volume), func.max(History.volume) - func.min(History.volume))
                 .filter(History.datetime>='2015-02-01')
                 .group_by(History.companies)
                 .order_by((func.max(History.volume) - func.min(History.volume)).desc())
                 .limit(10))
    s = s.all()

    print('%-15s%-15s%-15s%-15s' % ('stock', 'min', 'max', 'telda'))
    for i in s:
        print('%-15s%-15s%-15s%-15s' % (i[0].stock, '{0:,d}'.format(i[1]), '{0:,d}'.format(i[2]), '{0:,d}'.format(i[3])))
stock_engine = create_engine('mysql://root:@localhost/stock')
mubasher_engine = create_engine('mysql://root:@localhost/mubasher')

Session_S = scoped_session(sessionmaker(bind=stock_engine))
Session_M = scoped_session(sessionmaker(bind=mubasher_engine))

print('Stocks with highest volume')
StockWithHighestVolume()
print()
print('Stocks with most telda')
StockWithMostTelda()
