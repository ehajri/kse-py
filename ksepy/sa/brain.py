import click
from mubasher import *
from stock import *
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.sql import select
from datetime import date

@click.group()
def cli():
    pass

@cli.command()
@click.option('-k', '--kind', type=click.Choice(['high-vol', 'high-val', 'most-telda', 'most-trades']))
@click.option('-f', '--from-date', default='2013-01-01', metavar='start date')
@click.option('-t', '--to-date', default=date.today(), metavar='end date')
@click.pass_context
def show(ctx, kind, from_date, to_date):
    if kind is None:
        ctx.abort()
    
    click.echo('showing information from %s to %s' % (from_date, to_date))
    if kind == 'high-vol':
        StockWithHighestVolume(from_date, to_date)
    if kind == 'high-val':
        StockWithHighestValue(from_date, to_date)
    if kind == 'most-telda':
        StockWithMostTelda(from_date, to_date)
    if kind == 'most-trades':
        StockWithMostTrades(from_date, to_date)
    
    
def StockWithHighestVolume(from_date, to_date):
    """Stock with Highest Volume"""
    s = (Session_M.query(History, func.sum(History.volume))
                 .filter(History.datetime>=from_date)
                 .filter(History.datetime<=to_date)
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

def StockWithHighestValue(from_date, to_date):
    """Stock with Highest Value """
    s = (Session_M.query(History, func.sum(History.volume * (History.high + History.closing) / 2))
                 .filter(History.datetime>=from_date)
                 .filter(History.datetime<=to_date)
                 .group_by(History.companies)
                 .order_by(func.sum(History.volume * (History.high + History.closing) / 2).desc())
                 .limit(10))
    s = s.all()

    print('%-8s%-15s%-15s' % ('islamic', 'stock', 'value in KWD'))
    for i in s:
        if i[0].Company.islamic == 1:
            islamic = 'Yes'
        else:
            islamic = 'No'
        print('%-8s%-15s%-15s' % (islamic, i[0].stock, '{0:,g}'.format(i[1]/1000)))

def StockWithMostTelda(from_date, to_date):
    s = (Session_M.query(History, func.min(History.volume), func.max(History.volume), func.max(History.volume) - func.min(History.volume))
                 .filter(History.datetime>=from_date)
                 .filter(History.datetime<=to_date)
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

def StockWithMostTrades(from_date, to_date):
    s = (Session_M.query(History, func.min(History.volume), func.max(History.volume), func.max(History.volume) - func.min(History.volume))
                 .filter(History.datetime>=from_date)
                 .filter(History.datetime<=to_date)
                 .group_by(History.companies)
                 .order_by((func.max(History.volume) - func.min(History.volume)).desc())
                 .limit(10))
    s = s.all()

    print('%-15s%-15s%-15s%-15s' % ('stock', 'min', 'max', 'telda'))
    for i in s:
        print('%-15s%-15s%-15s%-15s' % (i[0].stock, '{0:,d}'.format(i[1]), '{0:,d}'.format(i[2]), '{0:,d}'.format(i[3])))

stock_engine = create_engine('mysql+pymysql://root:@localhost/stock')
mubasher_engine = create_engine('mysql+pymysql://root:@localhost/mubasher')

Session_S = scoped_session(sessionmaker(bind=stock_engine))
Session_M = scoped_session(sessionmaker(bind=mubasher_engine))
