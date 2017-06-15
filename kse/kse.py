import models
import func
import pymysql.cursors, peewee
import sys, os, time, datetime
import threading, logging
import stock_models as sm

from configobj import ConfigObj

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
logger = logging.getLogger(__name__)

config = ConfigObj('../config.ini')

lastruns = {'timesale': None, 'live': None, 'obook': None, 'news': None}


def ListToTuple(list):
    list2 = []
    for i in list:
        list2.append(tuple(i))
    return list2




def do_insert_news(records, fields):
    """
    :param records:
    :param fields (str):
    :return:
    """
    #fields = KeysToFields(fields)
    sql = "INSERT IGNORE INTO `News` (" + fields + ") VALUES (%s, %s, %s, %s)"

    #Store(records, sql)


def do_insert_timesale_pw(timesalelist, fields):
    data_source = [dict(zip(fields, t)) for t in timesalelist]
    with sm.db.atomic():
        for idx in range(0, len(data_source), 100):
            sm.Timesale.insert_many(data_source[idx:idx + 100]).execute()


def do_insert_livestock(livestocklist, fields):
    """
    :param livestocklist:
    :param fields (str):
    :return:
    """
    #fields = KeysToFields(fields)
    sql = "INSERT IGNORE INTO `RQuotes` (" + fields + ") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    #Store(livestocklist, sql)


def do_bulk_insert_pw(model, records, fields):
    """
    :param model:
    :param records:
    :param fields (list):
    :return:
    """
    data_source = [dict(zip(fields, t)) for t in records]
    with sm.db.atomic():
        for idx in range(0, len(data_source), 100):
            try:
                model.insert_many(data_source[idx:idx + 100]).execute()
            except peewee.IntegrityError:
                pass


def do_individual_insert_pw(model, records, fields):
    """
    :param model:
    :param records:
    :param fields (list):
    :return:
    """
    data_source = [dict(zip(fields, t)) for t in records]
    for record in data_source:
        try:
            model.insert(record).execute()
        except peewee.IntegrityError:
            logger.warning('%s is a duplicate', record)


def do_insert_obook_pw(obooklist, fields):
    """
    :param obooklist (list):
    :param fields (list):
    """
    data_source = [dict(zip(fields, t)) for t in obooklist]
    with sm.database.atomic():
        for idx in range(0, len(data_source), 100):
            sm.Obook.insert_many(data_source[idx:idx + 100]).execute()


def do_insert_obook(obooklist, fields):
    """
    :param obooklist (list):
    :param fields (str):
    """

    #fields = KeysToFields(fields)
    sql = "INSERT IGNORE INTO `OBook` (" + fields + ") VALUES (%s, %s, %s, %s, %s, %s, %s)"
    #Store(obooklist, sql)


def test():
    print("%s Hello" % datetime.datetime.today().now())


def Loop(f, interval):
    def inner():
        while True:
            try:
                f()
            except:
                pass
            finally:
                time.sleep(interval)
    return inner


class MyBaseModel:
    def __init__(self):
        self.time = None
        self.running_model = None
        self.Hello = 'bye'

    def update_last_run(self, time):
        self.running_model.lastrun = time
        self.running_model.save()

    def run(self):
        if self.time is None:
            self.time = datetime.datetime.now()

        diff = (datetime.datetime.now() - self.time).seconds
        if diff >= 10:
            self.time = datetime.datetime.now()
            self.update_last_run(self.time)
            self.execute()

    def execute(self):
        print('do nothing, base execute')


class OBookModel(MyBaseModel):
    def __init__(self, url, domId, running_model: sm.Running):
        super().__init__()
        self.url = url
        self.domId = domId
        self.fields = 'ticker price bid bid_qty ask ask_qty createdon'
        self.running_model = running_model

    def fetch(self):
        pageContent = func.FetchURL(self.url)
        return func.FetchOBook(pageContent, self.domId)

    def process(self, records):
        if records is None:
            logger.warning('OBook.process: no record passed')
            return

        for i, a in enumerate(records):
            # cleaning the records, and appending date at end of the record
            records[i] = [(float(x) if x else 0) for x in a]
            records[i].append(datetime.datetime.today().date())

        return records

    def save(self, records):
        logger.debug('OBook.save is called for %s records.', len(records))
        do_individual_insert_pw(sm.Obook, records, self.fields.split(' '))

    def execute(self):
        logger.debug('executing')
        records = self.fetch()
        records = self.process(records)
        self.save(records)

#funcs = [Job1, Job2, Job3, Job4]
obook_obj = OBookModel(config['obook']['url'], config['obook']['domId'], sm.Running.get(sm.Running.funcname == 'OBook'))
funcs = [obook_obj.run]


def dome():
    logger.debug('dome() is called')
    t = datetime.datetime.today()
    w = t.weekday()
    h = t.time().hour

    #logger.debug(funcs, obook_obj)

    if w == 4 or w == 5:
        logger.debug('Weekend!')
        return

    if h >= 15:
        logger.debug('too late!')
        return
    if h < 10:
        logger.debug('too early?')
        return

    logger.debug('show time! executing %s functions', str(funcs))

    for f in funcs:
        logger.debug('looping thru function at %s', 'hi')
        t = threading.Thread(target=f)
        t.daemon = True
        t.start()


def Process():
    logger.debug('Process started')
    Loop(dome, 10)()

print(obook_obj.__dict__)

if __name__ == '__main__':
    try:
        Process()
    except KeyboardInterrupt:
        print('Interrupt')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
