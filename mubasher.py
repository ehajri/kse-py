#!/usr/local/bin/python3
import pymysql.cursors
import requests, logging, sys, time
from configobj import ConfigObj
from random import randint
import json

logging.basicConfig(stream=sys.stderr, level=logging.WARNING)

config = ConfigObj('config.ini')

apis = ['amr', 'listed-companies', 'fairValues', 'capital-increase', 'earnings']
countries = ['kw', 'sa', 'ae', 'bh', 'om', 'qa', 'eg', 'jo', 'tn', 'ma', 'ps']
# countries = ['kw', 'sa', 'ae', 'bh', 'om', 'qa', 'eg', 'jo', 'tn', 'ma', 'ps', 'iq']


def makehost(uri, lang, args={}):
    if lang != 'ar' and lang != 'en':
        print('invalid language')
        return
    
    host = '.mubasher.info/api/1/'
    
    prefix = 'www' if lang == 'ar' else 'english'
    prefix = 'http://' + prefix
    
    url = prefix + host + uri
    
    querystring = []
    
    for i in args:
        querystring.insert(0, '{0}={1}'.format(i, args[i]))
    
    querystring = '?' + '&'.join(querystring)
    
    url = prefix + host + uri + querystring
    
    return url

def Fetch(url):
    try:
        time.sleep(randint(1, 7))
        r = requests.get(url)
        if r.status_code == requests.codes.ok:
            return r.json()
        else:
            print('%s %s' % (url, r.status_code))
    except Exception as e:
        print('Fetch Exception: %s %s' % (url, str(e)))

    return None

def func2():
    langs = ['ar']
    # langs = ['en', 'ar']
    for lang in langs:
        for country in countries:
            for api in apis:
                args = {'country': country}
                url = makehost(api, lang, args)
                print('Processing %s for %s in %s (%s)..' % (api, country, lang, url))
                p = Fetch(url)
                
                if p is None:
                    continue

                rows = p['rows']
                pages = p['numberOfPages']
                
                i = len(rows)
                j = pages * i
                
                if i == 0:
                    continue

                records = MakeRecords(rows, lang, url)
                StoreRecords(records)

                for start in range(i, j, i):
                    args['start'] = start
                    args['size'] = i

                    url = makehost(api, lang, args)
                    p = Fetch(url)
                
                    if p is None:
                        continue

                    rows = p['rows']
                    pages = p['numberOfPages']
                    
                    if len(rows) == 0:
                        continue
                    
                    records = MakeRecords(rows, lang, url)
                    StoreRecords(records)


def MakeRecords(listOfJson, lang, url):
    list = []
    for i in listOfJson:
        list.append((json.dumps(i), lang, url))
    return list

def StoreRecords(list):
    
    sql = "INSERT IGNORE INTO `jsons` (json, lang, uri) VALUES (%s, %s, %s)"

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
                logging.warning('affected rows is null!')
            elif affectedrows == 0:
                logging.warning('affected rows is 0!')
            else:
                logging.debug("Inserted %d rows", affectedrows)

        connection.commit()
    finally:
        connection.close()

func2()

# below is a list of apis which supports both paging and country
# 
# listed-companies ==> country
# amr (same)
# fairValues
# capital-increase
# earnings => year!
# 
# stocks/prices/all or /? gives "lastUpdate" and "prices" => []

# http://www.mubasher.info/api/1/events?countries=kw&from=2015-05-23&to=2015-05-30
