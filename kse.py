#!/usr/local/bin/python3

import models
import datetime
import func
import pymysql.cursors
import sys
import time
import os
from configobj import ConfigObj

config = ConfigObj('config.ini')

def ListToTuple(list):
    list2 = []
    for i in list:
        list2.append(tuple(i))
    return list2

def UpdateRunning(str):
    connection = pymysql.connect(host=config['db']['host'],
                             user=config['db']['user'],
                             passwd=config['db']['pass'],
                             db=config['db']['dbname'],
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
            print("Inserted %d rows" % affectedrows)

        connection.commit()
    finally:
        connection.close()

def LiveStock():
    print("%s Live Stock Listener started!" % datetime.datetime.now().time())
    pageContent = func.FetchURL(config['rquotes']['url'])

    list = func.FetchRQuotes(pageContent, config['rquotes']['domId'])

    if list == None:
        print("Nothing returned from FetchRQuotes")
    else:
        #list.append([507, 108.000, 8.000, 108.000, 108.000, 108.000, 1, 2, 108.000, 100.000, 100.000, '2017-04-15', 96.000, 0.000]);
        sql = "INSERT IGNORE INTO `RQuotes` (`ticker_id`, `last`, `change`, `open`, `high`, `low`, `vol`, `trade`, `value`, `prev`, `ref`, `prev_date`, `bid`, `ask`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        Store(list, sql)

def News():
    print("%s News Listener started!" % datetime.datetime.now().time())
    pageContent = func.FetchURL(config['news']['url1'])

    list = func.FetchNews(pageContent, config['news']['domId1'])

    if list == None:
        print("News did not return anything")
        return

    for i in list:
        i[2] = i[2].strftime('%Y-%m-%d %H:%M:%S')
        pageContent = func.FetchURL(config['news']['url2'] + str(i[0]))
        temp = func.FetchArticle(pageContent, config['news']['domId2'])
        if temp == None:
            print("%d returned none" %i[0])
        else:
            i.append(temp)

    sql = "INSERT IGNORE INTO `News` (`newsid`, `headline`, `date`, `message`) VALUES (%s, %s, %s, %s)"

    Store(list, sql)

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
    print("%s OBook Listener started!" % datetime.datetime.now().time())
    pageContent = func.FetchURL(config['obook']['url'])

    list = func.FetchOBook(pageContent, config['obook']['domId'])

    for i, a in enumerate(list):
        list[i] = [(float(x) if x else 0) for x in a]
        list[i].append(datetime.datetime.today().date())

    fields = KeysToFields('ticker_id price bid bid_qty ask ask_qty createdon')

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
    print("%s TimeSale Listener started!" % datetime.datetime.now().time())

    pageContent = func.FetchURL(config['timesale']['url2'])

    list = func.FetchTimeSale2(pageContent, config['timesale']['domId2'])

    if list == None:
        print("Nothing returned from FetchTimeSale2")
    elif len(list) == 0:
        print("0 record returned from FetchTimeSale2")
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
            UpdateRunning(str(f).split(' ')[1])
            f()
        except:
            pass
        finally:
            time.sleep(interval)
  return inner


def Process():
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
