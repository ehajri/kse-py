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

apis = ['listed-companies', 'amr', 'fairValues', 'capital-increase', 'earnings', 'stocks/prices']
countries = ['kw', 'sa']

def makehost(uri, lang='ar', c='kw', size=20, start=0, extra='', plain=False):
    if lang != 'ar' and lang != 'en':
        print('invalid language')
        return

    host = '.mubasher.info/api/1/'

    prefix = 'www' if lang == 'ar' else 'english'
    prefix = 'http://' + prefix

    url = prefix + host + uri
    if not plain:
        url += '?country=' + c + '&size=' + str(size) + '&start=' + str(start) + '&' + extra
    
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
    for api in apis:
        print('Processing %s..' % api)
        url = makehost(api, 'en', {})
        p = func(url)
        rows = p['rows']
        pages = p['numberOfPages']
        
        i = len(rows)
        j = pages * i
        
        for start in range(i, j, i):
            d = {size: i, start: start}
            h = makehost(api, size=i, start=start)
            print(h)
        break

# 1 item = 1 page, 2 items = 1 page, 20 items = 1 page, 21 = 2 pages

func2()

# http://www.mubasher.info/api/1/events?countries=kw&from=2015-05-23&to=2015-05-30
# http://www.mubasher.info/api/1/stocks/prices?country=kw
# http://www.mubasher.info/api/1/stocks/prices/all?country=kw
# http://www.mubasher.info/api/1/ipos?country=kw
# http://www.mubasher.info/api/1/earnings?country=kw
# http://www.mubasher.info/api/1/earnings?country=kw&size=20&start=20
# http://www.mubasher.info/api/1/earnings?country=kw&year=2012
# http://www.mubasher.info/api/1/earnings?country=kw&size=20&start=80&year=2012
