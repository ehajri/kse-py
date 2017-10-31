from peewee import *

database = MySQLDatabase('ksehistory', **{'user': 'root'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Company(BaseModel):
    name = CharField()
    sector = CharField()
    stk = IntegerField()
    ticker = CharField()

    class Meta:
        db_table = 'company'

