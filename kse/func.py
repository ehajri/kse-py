import requests
import datetime, sys, logging
from bs4 import BeautifulSoup


logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

def FetchURL(link):
    "Reads the URL and fetch its content"
    f = requests.get(link)
    soup = BeautifulSoup(f.text, 'html.parser')
    return soup

def FetchRQuotes(soup, id):
    "Fetches RQuotes records from a soup object"
    table = soup.find(id=id)

    if not table or table is None:
        return None

    trs = table.findAll('tr')

    if trs is None or len(trs) == 0:
        return None

    trs.pop(0)
    list = []
    for tr in trs:
        tds = tr.findAll('td')
        temp = []

        td = tds.pop(0)
        temp.append(td.a['href'].split('=')[1])

        for td in tds:
            temp.append(Sanitize(td.text))
        temp = ChangeTypes(temp)
        list.append(temp)
    return list

def FetchNews(soup, id):
    "Fetches RQuotes records from a soup object"
    table = soup.find(id=id)
    trs = table.findAll('tr')
    if len(trs) < 2:
        return None
    trs.pop(0)
    list = []
    for tr in trs:
        tds = tr.findAll('td')

        # 1st td is expected to be something like <td>09:24:35</td>
        time = Sanitize(tds.pop(0).text).split(':')
        # convert the list of strings to list of ints
        time = [int(i) for i in time]
        # return an time object
        time = datetime.time(time[0], time[1], time[2])

        #dt = datetime.datetime(2015, 4, 30)
        dt = datetime.datetime.now()

        date = datetime.datetime.combine(dt, time)

        # 2nd td is expected to be something like <td><a href='..id=..'>headline</a></td>
        a        = tds.pop(0).a
        newsid   = a['href'].split('=')[1]
        headline = Sanitize(a.text)

        list.append([int(newsid), headline, date])
    return list

def FetchOBook(soup, id):
    "Fetches Orders Book from a soup object"
    table = soup.find(id=id)

    if table is None:
        return None
    #print(table)
    trs = table.findAll('tr')
    if trs is None:
        return None
    #print(trs)
    trs.pop(0)
    list = []
    for tr in trs:
        temp = []
        # 1st td has the ticker id, so let's fetch it
        tds = tr.findAll('td')
        a        = tds.pop(0).a
        ticker   = a['href'].split('=')[1].split('&')[0]
        temp.append(ticker)

        # get the rest of the tds
        for td in tds:
            temp.append(Sanitize(td.text))
        list.append(temp)
    return list

def FetchArticle(soup, id):
    "Fetches single article from a soup object"
    div = soup.find(id=id)
    if div == None:
        return None
    return div.text.strip()

def FetchTimeSale(soup, id):
    "Fetches time and sale from a soup object"
    table = soup.find(id=id)

    trs = table.findAll('tr')
    trs.pop(0)
    trs.pop(len(trs)-1)
    list = []
    for tr in trs:
        tds = tr.findAll('td')
        tds.pop(0)
        price = Sanitize(tds.pop(0).text)
        price = float(price)
        quantity = Sanitize(tds.pop(0).text)
        quantity = float(quantity)
        time = Sanitize(tds.pop(0).text)

        # 1st td is expected to be something like <td>09:24:35</td>
        time = time.split(':')
        # convert the list of strings to list of ints
        time = [int(i) for i in time]
        # return an time object
        time = datetime.time(time[0], time[1], time[2])

        #dt = datetime.datetime(2015, 4, 30)
        dt = datetime.datetime.now()

        date = datetime.datetime.combine(dt, time)

        list.append([price, quantity, date])

    return list

def FetchTimeSale2(soup, id):
    "Fetches time and sale from a soup object"
    table = soup.find(id=id)

    if table is None:
        return None

    trs = table.findAll('tr')

    if trs is None or len(trs) == 1:
        return None

    trs.pop(0)
    trs.pop(len(trs)-1)
    list = []
    for tr in trs:
        tds = tr.findAll('td')
        a        = tds.pop(0).a
        ticker   = a['href'].split('=')[1].split('&')[0]
        ticker   = int(ticker)

        price = Sanitize(tds.pop(0).text)
        price = float(price)
        quantity = Sanitize(tds.pop(0).text)
        quantity = float(quantity)
        time = Sanitize(tds.pop(0).text)

        # 1st td is expected to be something like <td>09:24:35</td>
        time = time.split(':')
        # convert the list of strings to list of ints
        time = [int(i) for i in time]
        # return an time object
        time = datetime.time(time[0], time[1], time[2])

        #dt = datetime.datetime(2015, 4, 30)
        dt = datetime.datetime.now()

        date = datetime.datetime.combine(dt, time)

        list.append([ticker, price, quantity, date])

    return list

def Sanitize(str):
    return str.strip().replace(',', '')

def ChangeTypes(list):
    try:
        for i in [0, 6, 7]:
            list[i] = 0 if not list[i] else int(list[i])
        for i in [1, 2, 3, 4, 5, 8, 9, 10, 12, 13]:
            list[i] = 0 if not list[i] else float(list[i])

        list[11] = datetime.datetime.strptime(list[11], "%d-%m-%Y").date()
        return list
    except:
        logging.warning(list)
        pass
    return None


def MakeDict(list, names):
    listofdict = []
    for outer in list:
        dict = {}
        for i, r in enumerate(outer):
            dict[names[i]] = r
        listofdict.append(dict)
    return listofdict
