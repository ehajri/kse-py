from stock import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
stock_engine = create_engine('mysql://root:@localhost/stock')

Session = sessionmaker(bind=stock_engine)
session = Session()

objs = session.query(Running).all()

print(len(objs))
