#!/usr/local/bin/python3
import requests

# link = 'mo'
# r = requests.get(link)
# 
# if r.status_code == requests.codes.ok:
#     try:
#         # print(r.text)
#         # print(r.json())
#         # print(o)
#         v = 1
#     except Exception as inst:
#         print(type(inst))     # the exception instance
#         print(inst.args)      # arguments stored in .args
#         print(inst)
#         pass

apis = ['listed-companies', 'amr', 'fairValues', 'capital-increase', 'earnings']
countries = ['kw', 'sa']

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

def func(url):
    print('fetching %s..' % url)

    try:
        r = requests.get(url)
        j = r.json()
        if ('rows' not in j and 'numberOfPages' not in j) or len(j) != 2:
            print('need manual check')
        if 'rows' in j:
            print('rows: %d' % len(j['rows']))
        if 'numberOfPages' in j:
            print('pages: %d' % j['numberOfPages'])
        
        return j
    except:
        print('error')
        pass

    return

def func2():
    country = 'kw'
    lang = 'en'
    args = {'country': country}
    for api in apis:
        print('Processing %s..' % api)
        url = makehost(api, 'en', args)
        p = func(url)
        rows = p['rows']
        pages = p['numberOfPages']
        
        i = len(rows)
        j = pages * i
        
        for start in range(i, j, i):
            args['start'] = start
            args['size'] = i
            d = {'size': i, 'start': start}
            h = makehost(api, lang, args)
            print(h)
        break

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
