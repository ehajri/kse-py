#!/usr/local/bin/python3

from datetime import datetime
from bs4 import BeautifulSoup
from configobj import ConfigObj
import pymysql.cursors, json, requests, sys, logging


logging.basicConfig(stream=sys.stderr, level=logging.WARNING)

config = ConfigObj('config.ini')

def StockDetail(soup):
    s = soup.find(class_='stock-overview__text-and-value-items')
    o = {}
    for div in s.children:
        if div.name is None:
            continue
        l = [span.text.strip().replace('\n', ' ') for span in div.children if span.name is not None]
        key   = l[0]
        value = l[1] # inner text
        if key != 'Trading Currency':
            value = value.split(' ')[0] # just take the figure
            value = value.replace(',', '').replace('%', '')
        o[key] = value
    return o

def HistoryURL(soup):
    return soup.find(class_='market__chart md-whiteframe-z1')['historical-data-url']

def Statistics(soup):
    s = soup.find(class_='stock-overview__text-and-value')
    o = {}
    for div in s.children:
        if div.name is None:
            continue
        l = [span.text.strip().replace('\n', ' ') for span in div.children if span.name is not None]
        o[l[0]] = l[1].replace(',', '')
    return o

def str_to_datetime(str):
    return datetime.strptime(str, '%Y-%m-%d/%H:%M:%S')

def PrepareHistory(text):
    lines = (line.split(',') for line in text.split('\n') if line != '')
    fields = ((str_to_datetime(line[0]), line[1], line[2], line[3], line[4], line[5]) for line in lines)
    
    result = []
    for item in fields:
        result.append(item)
    
    return result

def StoreInfo(symbol, detail, stat):
    sql  = 'INSERT INTO `stocks` (stock, pb_ratio, market_cap, total_assets_growth_percentage, pe_ratio, book_value, eps, par_value, currency, capital, total_share) '
    sql += 'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    d    = detail
    s    = stat
    t    = (symbol, d['P/B Ratio'], d['Market Cap'], d['Total Assets Growth %'], d['P/E Ratio'], d['Book Value'], d['EPS'], d['Par Value'], d['Trading Currency'], s['Company Capital'], s['Current Total Shares'])
    
    PutRecords(sql, [t])
    
def StoreHistory(symbol, records):
    sql  = 'INSERT IGNORE INTO `history` (stock, `datetime`, open, high, low, closing, volume) '
    sql += "VALUES ('" + symbol + "', %s, %s, %s, %s, %s, %s)"
    
    PutRecords(sql, records)

def RemoveCommas(arg):
    for i, j in enumerate(arg):
        if type(arg[j]) is str:
            arg[j] = arg[j].replace(',', '')
    return arg

def Main():
    records = GetRecords()
    url = 'http://english.mubasher.info'
    
    for record in records:
        jsonobj = json.loads(record['json'])

        symbol = jsonobj['symbol']

        print('Processing %s...' % symbol)

        targethost = url + jsonobj['url']
        
        r = requests.get(targethost)
        if r.status_code == requests.codes.ok:
            soup = BeautifulSoup(r.text)

            stockDetail = StockDetail(soup)
            statistics  = Statistics(soup)
            hsitoryURL  = HistoryURL(soup)
            
            # print(stockDetail)
            # print(statistics)
            
            StoreInfo(symbol, stockDetail, statistics)
            
            r = requests.get(HistoryURL(soup))
            if r.status_code == requests.codes.ok:
                ph = PrepareHistory(r.text)
                StoreHistory(symbol, ph)
                # print('# of history is: %d' % len(ph))
            else:
                print('%s something is wrong[2]' % r.status_code)
        else:
            print('%s something is wrong[1]' % r.status_code)
        print()

def GetRecords():
    result = []
    connection = pymysql.connect(host=config['db']['host'],
                             user=config['db']['user'],
                             passwd=config['db']['pass'],
                             db=config['db']['dbname2'],
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM jsons WHERE lang = 'en' AND uri LIKE '%listed-companies%kw%'")
            result = cursor.fetchall()
        connection.commit()
    finally:
        connection.close()
        return result

def PutRecords(sql, list):
    connection = pymysql.connect(host=config['db']['host'],
                             user=config['db']['user'],
                             passwd=config['db']['pass'],
                             db=config['db']['dbname2'],
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            affectedrows = cursor.executemany(sql, list)
            if affectedrows is None:
                loggin.warning('affected rows is null!')
            else:
                logging.debug("Inserted %d rows", affectedrows)

        connection.commit()
    finally:
        connection.close()

Main()

# URC GLOBAL
