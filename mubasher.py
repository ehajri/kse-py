#!/usr/local/bin/python3
import requests

apis = ['listed-companies', 'amr', 'fairValues', 'capital-increase', 'earnings']
countries = ['kw', 'sa', 'ae', 'bh', 'om', 'qa', 'eg', 'jo', 'tn', 'ma', 'ps','iq']

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
        r = requests.get(url)
        if r.status_code == requests.codes.ok:
            return r.json()
        else:
            print('%s %s' % (url, r.status_code))
    except Exception as e:
        print('Fetch Exception: %s %s' % (url, str(e)))

    return None

def func2():
    langs = ['ar', 'en']
    for lang in langs:
        for country in countries:
            args = {'country': country}
            for api in apis:
                print('Processing %s for %s in %s..' % (api, country, lang))

                url = makehost(api, lang, args)
                p = Fetch(url)
                
                if p is None:
                    continue

                rows = p['rows']
                pages = p['numberOfPages']
                
                Store(rows)
                
                i = len(rows)
                j = pages * i
                
                for start in range(i, j, i):
                    args['start'] = start
                    args['size'] = i
                    d = {'size': i, 'start': start}

                    url = makehost(api, lang, args)
                    p = Fetch(url)
                    print(h)
                break

def Store(jsons):

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
            elif affectednow
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
