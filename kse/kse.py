import models
import func
import pymysql.cursors
import sys, os, time, datetime
import threading, logging
import stock_models as sm

from configobj import ConfigObj

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
logger = logging.getLogger(__name__)

config = ConfigObj('../config.ini')

lastruns = { 'timesale': None, 'live': None, 'obook': None, 'news': None }


def ListToTuple(list):
    list2 = []
    for i in list:
        list2.append(tuple(i))
    return list2


def UpdateRunning(str):
    record = sm.Running.get(sm.Running.funcname == str)
    record.lastrun = datetime.datetime.now()
    record.save()


def GetTickersPW():
    tickers = sm.Tickers.select()
    return tickers


def GetTickers():
    result = []
    connection = pymysql.connect(host=config['db']['host'],
                                 user=config['db']['user'],
                                 passwd=config['db']['pass'],
                                 db=config['db']['dbnane'],
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Tickers")
            result = cursor.fetchall()
        connection.commit()
    finally:
        connection.close()
        return result


def Store(list, sql):
    list = ListToTuple(list)

    connection = pymysql.connect(host=config['db']['host'],
                             user=config['db']['user'],
                             passwd=config['db']['pass'],
                             db=config['db']['dbname'],
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            affectedrows = cursor.executemany(sql, list)
            if affectedrows is None:
                logger.warning('affected rows is null!')
            else:
                logger.debug("Inserted %d rows", affectedrows)

        connection.commit()
    finally:
        connection.close()


def LiveStock():
    logger.info("%s Live Stock Listener started!", datetime.datetime.now().time())
    pageContent = func.FetchURL(config['rquotes']['url'])

    livestocklist = func.FetchRQuotes(pageContent, config['rquotes']['domId'])

    if livestocklist is None:
        logger.warning("Nothing returned from FetchRQuotes")
    else:
        #list.append([507, 108.000, 8.000, 108.000, 108.000, 108.000, 1, 2, 108.000, 100.000, 100.000, '2017-04-15', 96.000, 0.000]);
        livestocklist = [x for x in livestocklist if all(xx != 0 for xx in x[1:9])]

        fields = 'ticker_id last change open high low vol trade value prev ref prev_date bid ask'

        # do_insert_livestock(livestocklist, fields)
        do_insert_pw(sm.Rquotes, livestocklist, fields.split(' '))


def News():
    logger.info("%s News Listener started!" % datetime.datetime.now().time())
    pageContent = func.FetchURL(config['news']['url1'])

    records = func.FetchNews(pageContent, config['news']['domId1'])

    if records is None:
        logger.warning("News did not return anything")
        return

    for i in records:
        if NewsExists(i[0], i[2]):
            records.remove(i)

    for i in records:
        i[2] = i[2].strftime('%Y-%m-%d %H:%M:%S')
        pageContent = func.FetchURL(config['news']['url2'] + str(i[0]))
        temp = func.FetchArticle(pageContent, config['news']['domId2'])
        if temp is None:
            logger.warning("%d returned none" % i[0])
        else:
            # print("%d to insert" % i[0])
            i.append(temp)

    fields = "newsid headline date message"

    # do_insert_news(records, fields)
    do_insert_pw(sm.News, records, fields.split(' '))


def NewsExists(article_id, article_date):
    count = sm.News.select().where(sm.News.id == article_id and sm.News.date == article_date).count()
    return count > 0


# not used?


def GetTodays(section):
    table = ''
    if section == 'obook':
        table = 'OBook'

    if table == '':
        print('GetTodays is passed with an invalid section')
        return None

    number_of_rows = 0
    connection = pymysql.connect(host=config['db']['host'],
                             user=config['db']['user'],
                             passwd=config['db']['pass'],
                             db=config['db']['db'],
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            sql = "SELECT COUNT(*) AS total FROM {0} WHERE `timestamp` > CURRENT_DATE".format(table)
            cursor.execute(sql)
            number_of_rows = cursor.fetchone()['total']

        connection.commit()
    finally:
        connection.close()
        return number_of_rows

def OBook():
    logger.info("%s OBook Listener started!" % datetime.datetime.now().time())
    pageContent = func.FetchURL(config['obook']['url'])

    obooklist = func.FetchOBook(pageContent, config['obook']['domId'])

    if obooklist is None:
        logger.debug('OBook returned nothing')
        return

    for i, a in enumerate(obooklist):
        obooklist[i] = [(float(x) if x else 0) for x in a]
        obooklist[i].append(datetime.datetime.today().date())

    fields = 'ticker_id price bid bid_qty ask ask_qty createdon'

    if len(obooklist) == 0:
        logger.debug('OBook has no records')
        return

    logger.debug('OBook has ' + len(obooklist) + ' and inserting them..')

    do_insert_obook_pw(obooklist, fields.split(' '))


def KeysToFields(str):
    list = str.split(' ')
    str = ', '.join("`{0}`".format(w) for w in list)
    return str

# not sure what this is doing


def TimeSale2():
    tickers = GetTickers()

    list = []
    for ticker in tickers:
        pageContent = func.FetchURL(config['timesale']['url'] % ticker['ticker_id'])
        temp = func.FetchTimeSale(pageContent, config['timesale']['domId'])
        if temp:
            for i, a in enumerate(temp):
                a.append(ticker['ticker_id'])
            list = list + temp

    fields = KeysToFields('price quantity datetime ticker_id')
    sql = "INSERT IGNORE INTO `TimeSale` (" + fields + ") VALUES (%s, %s, %s, %s)"

    Store(list, sql)


def TimeSale():
    logger.info("%s TimeSale Listener started!" % datetime.datetime.now().time())

    pageContent = func.FetchURL(config['timesale']['url2'])

    timesalelist = func.FetchTimeSale2(pageContent, config['timesale']['domId2'])

    if timesalelist is None:
        logger.warning("Nothing returned from FetchTimeSale2")
    elif len(list) == 0:
        logger.warning("0 record returned from FetchTimeSale2")
    else:
        fields = 'ticker_id price quantity datetime'
        # do_insert_timesale(timesalelist, fields)
        do_insert_timesale_pw(timesalelist, fields.split(' '))


def do_insert_news(records, fields):
    """
    :param records:
    :param fields (str):
    :return:
    """
    fields = KeysToFields(fields)
    sql = "INSERT IGNORE INTO `News` (" + fields + ") VALUES (%s, %s, %s, %s)"

    Store(records, sql)


def do_insert_timesale_pw(timesalelist, fields):
    data_source = [dict.zip(fields, t) for t in timesalelist]
    with sm.atomic():
        for idx in range(0, len(data_source), 100):
            sm.Timesale.insert_many(data_source[idx:idx + 100]).execute()


def do_insert_livestock(livestocklist, fields):
    """
    :param livestocklist:
    :param fields (str):
    :return:
    """
    fields = KeysToFields(fields)
    sql = "INSERT IGNORE INTO `RQuotes` (" + fields + ") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    Store(livestocklist, sql)


def do_insert_pw(model, records, fields):
    """
    :param model:
    :param records:
    :param fields (list):
    :return:
    """
    data_source = [dict.zip(fields, t) for t in records]
    with sm.atomic():
        for idx in range(0, len(data_source), 100):
            model.insert_many(data_source[idx:idx + 100]).execute()


def do_insert_obook_pw(obooklist, fields):
    """
    :param obooklist (list):
    :param fields (list):
    """
    data_source = [dict.zip(fields, t) for t in obooklist]
    with sm.atomic():
        for idx in range(0, len(data_source), 100):
            sm.OBook.insert_many(data_source[idx:idx + 100]).execute()


def do_insert_obook(obooklist, fields):
    """
    :param obooklist (list):
    :param fields (str):
    """

    fields = KeysToFields(fields)
    sql = "INSERT IGNORE INTO `OBook` (" + fields + ") VALUES (%s, %s, %s, %s, %s, %s, %s)"
    Store(obooklist, sql)


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


def Process():
    Loop(dome, 10)()


def dome():
    t = datetime.datetime.today()
    w = t.weekday()
    h = t.time().hour

    if w == 4 or w == 5:
        logger.debug('Weekend!')
        return

    if h >= 15:
        logger.debug('too late!')
        return
    if h < 8:
        logger.debug('too early?')
        return

    logger.debug('show time!')

    for f in funcs:
        t = threading.Thread(target=f)
        t.daemon = True
        t.start()


def Job1():
    if lastruns['timesale'] is None:

        lastruns['timesale'] = datetime.datetime.now()

    diff = (datetime.datetime.now() - lastruns['timesale']).seconds
    if diff >= 10:
        lastruns['timesale'] = datetime.datetime.now()
        UpdateRunning('TimeSale')
        TimeSale()


def Job2():
    if lastruns['live'] is None:
        lastruns['live'] = datetime.datetime.now()

    diff = (datetime.datetime.now() - lastruns['live']).seconds
    if diff >= 10:
        lastruns['live'] = datetime.datetime.now()
        UpdateRunning('LiveStock')
        LiveStock()


def Job3():
    if lastruns['news'] is None:
        lastruns['news'] = datetime.datetime.now()

    diff = (datetime.datetime.now() - lastruns['news']).seconds
    if diff >= 60:
        lastruns['news'] = datetime.datetime.now()
        UpdateRunning('News')
        News()


def Job4():
    if lastruns['obook'] is None:
        lastruns['obook'] = datetime.datetime.now()

    diff = (datetime.datetime.now() - lastruns['obook']).seconds
    if diff >= 10:
        lastruns['obook'] = datetime.datetime.now()
        UpdateRunning('OBook')
        OBook()


#funcs = [Job1, Job2, Job3, Job4]
funcs = [Job4]


def Process2():
    if len(sys.argv) < 2:
        print('No argument found.. terminating!')
    else:
        cmd = sys.argv[1]
        option = None
        interval = None
        if len(sys.argv) == 4:
            option = sys.argv[2]
            interval = int(sys.argv[3])

        func = None

        if cmd == 'live':
            func = LiveStock
        elif cmd == 'bye':
            print('Later!')
        elif cmd == 'help':
            print("Usage:")
            print("%s <cmd> [option]" % sys.argv[0])
            print("Available commands:")
            print("\thelp")
            print("\tlive")
            print("\tnews")
            print("\tobook")
            print("\ttimesale")
            print("\ttest")
            print("\tbye")
            print("Available options:")
            print("\t--loop\t:run continuously")
        elif cmd == 'news':
            func = News
        elif cmd == 'obook':
            func = OBook
        elif cmd == 'timesale':
            func = TimeSale
        elif cmd == 'test':
            func = test
        else:
            print('unknown command. try help')
        if func:
            if option and interval and option == '--loop':
                func2 = func
                func = Loop(func2, interval)
            func()

if __name__ == '__main__':
    try:
        Process()
    except KeyboardInterrupt:
        print('Interrupt')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
