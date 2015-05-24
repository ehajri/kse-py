#!/usr/local/bin/python3

import anyjson
import requests

link = mo
r = requests.get(link)

if r.status_code == requests.codes.ok:
    try:
        # print(r.text)
        # print(r.json())
        o = anyjson.deserialize(r.json())
        # print(o)
    except Exception as inst:
        print(type(inst))     # the exception instance
        print(inst.args)      # arguments stored in .args
        print(inst)
        pass

def func(uri, lang='ar', c='kw', size=20, start=0, extra='', plain=False):
    if lang != 'ar' and lang != 'en':
        print('invalid language')
        return
    
    host = '.mubasher.info/api/1/'
    
    prefix = 'www' if lang == 'ar' else 'english'
    prefix = 'http://' + prefix
    
    url = prefix + host + uri
    if not plain:
        url += '?country=' + c + '&size=' + str(s) + '&' + extra
    
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
    except:
        print('error')
        pass
        
    return

apis = ['listed-companies', 'amr', 'fairValues', 'capital-increase', 'earnings', ]

# http://www.mubasher.info/api/1/events?countries=kw&from=2015-05-23&to=2015-05-30
# http://www.mubasher.info/api/1/listed-companies?country=kw
# http://www.mubasher.info/api/1/listed-companies?country=kw&size=20&start=20
# http://www.mubasher.info/api/1/amr?country=kw
# http://www.mubasher.info/api/1/amr?country=kw&size=20&start=20
# http://www.mubasher.info/api/1/stocks/prices?country=kw
# http://www.mubasher.info/api/1/stocks/prices/all?country=kw
# http://www.mubasher.info/api/1/fairValues?country=kw
# http://www.mubasher.info/api/1/fairValues?country=kw&size=20&start=20
# http://www.mubasher.info/api/1/ipos?country=kw
# http://www.mubasher.info/api/1/earnings?country=kw
# http://www.mubasher.info/api/1/earnings?country=kw&size=20&start=20
# http://www.mubasher.info/api/1/earnings?country=kw&year=2012
# http://www.mubasher.info/api/1/earnings?country=kw&size=20&start=80&year=2012
# http://www.mubasher.info/api/1/capital-increase?country=kw
# http://www.mubasher.info/api/1/capital-increase?country=kw&size=20&start=20
# 
# 
# 
# earnings?country=kw&size=20&start=80&year=2012
