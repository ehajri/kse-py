import models
import func
import pymysql.cursors
import sys, os, time, datetime
import threading, logging

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
    connection = pymysql.connect(host=os.environ['MYSQL_PORT_3306_TCP_ADDR'],
                                 user='root',
                                 passwd=os.environ['MYSQL_ENV_MYSQL_ROOT_PASSWORD'],
                                 db='stock',
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            cursor.execute("UPDATE running SET lastrun = %s WHERE funcname = %s", (datetime.datetime.now(), str))
            result = cursor.fetchall()
        connection.commit()
    finally:
        connection.close()
        return result

def GetTickers():
    result = []
    connection = pymysql.connect(host=os.environ['MYSQL_PORT_3306_TCP_ADDR'],
                                 user='root',
                                 passwd=os.environ['MYSQL_ENV_MYSQL_ROOT_PASSWORD'],
                                 db='stock',
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

    connection = pymysql.connect(host=os.environ['MYSQL_PORT_3306_TCP_ADDR'],
                                 user='root',
                                 passwd=os.environ['MYSQL_ENV_MYSQL_ROOT_PASSWORD'],
                                 db='stock',
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

    list = func.FetchRQuotes(pageContent, config['rquotes']['domId'])

    if list == None:
        logger.warning("Nothing returned from FetchRQuotes")
    else:
        #list.append([507, 108.000, 8.000, 108.000, 108.000, 108.000, 1, 2, 108.000, 100.000, 100.000, '2017-04-15', 96.000, 0.000]);
        list = [x for x in list if all(xx != 0 for xx in x[1:9])]

        sql = "INSERT IGNORE INTO `RQuotes` (`ticker_id`, `last`, `change`, `open`, `high`, `low`, `vol`, `trade`, `value`, `prev`, `ref`, `prev_date`, `bid`, `ask`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        Store(list, sql)

def News():
    logger.info("%s News Listener started!" % datetime.datetime.now().time())
    pageContent = func.FetchURL(config['news']['url1'])

    list = func.FetchNews(pageContent, config['news']['domId1'])

    if list == None:
        logger.warning("News did not return anything")
        return

    for i in list:
        if NewsExists(i[0], i[2]):
            list.remove(i)

    for i in list:
        i[2] = i[2].strftime('%Y-%m-%d %H:%M:%S')
        pageContent = func.FetchURL(config['news']['url2'] + str(i[0]))
        temp = func.FetchArticle(pageContent, config['news']['domId2'])
        if temp == None:
            logger.warning("%d returned none" % i[0])
        else:
            # print("%d to insert" % i[0])
            i.append(temp)

    sql = "INSERT IGNORE INTO `News` (`newsid`, `headline`, `date`, `message`) VALUES (%s, %s, %s, %s)"

    Store(list, sql)

def NewsExists(article_id, article_date):
    connection = pymysql.connect(host=os.environ['MYSQL_PORT_3306_TCP_ADDR'],
                                 user='root',
                                 passwd=os.environ['MYSQL_ENV_MYSQL_ROOT_PASSWORD'],
                                 db='stock',
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            sql = "SELECT COUNT(*) AS total FROM News WHERE `newsid` = {0} AND `date` = '{1}'".format(article_id, article_date)
            cursor.execute(sql)
            number_of_rows = cursor.fetchone()['total']
        connection.commit()
    finally:
        connection.close()
        return number_of_rows > 0

# not used?


def GetTodays(section):
    table = ''
    if section == 'obook':
        table = 'OBook'

    if table == '':
        print('GetTodays is passed with an invalid section')
        return None

    number_of_rows = 0
    connection = pymysql.connect(host=os.environ['MYSQL_PORT_3306_TCP_ADDR'],
                                 user='root',
                                 passwd=os.environ['MYSQL_ENV_MYSQL_ROOT_PASSWORD'],
                                 db='stock',
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

    list = func.FetchOBook(pageContent, config['obook']['domId'])

    if list is None:
        return

    for i, a in enumerate(list):
        list[i] = [(float(x) if x else 0) for x in a]
        list[i].append(datetime.datetime.today().date())

    fields = KeysToFields('ticker_id price bid bid_qty ask ask_qty createdon')

    if len(list) == 0:
        return

    sql = "INSERT IGNORE INTO `OBook` (" + fields + ") VALUES (%s, %s, %s, %s, %s, %s, %s)"
    Store(list, sql)

def KeysToFields(str):
    list = str.split(' ')
    str = ', '.join("`{0}`".format(w) for w in list)
    return str

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

    list = func.FetchTimeSale2(pageContent, config['timesale']['domId2'])

    if list == None:
        logger.warning("Nothing returned from FetchTimeSale2")
    elif len(list) == 0:
        logger.warning("0 record returned from FetchTimeSale2")
    else:
        fields = KeysToFields('ticker_id price quantity datetime')
        sql = "INSERT IGNORE INTO `TimeSale` (" + fields + ") VALUES (%s, %s, %s, %s)"
        Store(list, sql)

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
    if h < 10:
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

funcs = [Job1, Job2, Job3, Job4]
#funcs = [Job2]
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
