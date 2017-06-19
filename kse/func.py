import requests
import datetime, sys, logging
from bs4 import BeautifulSoup


def fetch_url(link):
    """Reads the URL and fetch its content"""
    f = requests.get(link)
    soup = BeautifulSoup(f.text, 'html.parser')
    return soup


def fetch_rquotes(soup, id):
    """Fetches RQuotes records from a soup object"""
    table = soup.find(id=id)

    if not table or table is None:
        return None

    trs = table.findAll('tr')

    if trs is None or len(trs) == 0:
        return None

    trs.pop(0)
    records = []
    for tr in trs:
        tds = tr.findAll('td')
        temp = []

        td = tds.pop(0)
        temp.append(td.a['href'].split('=')[1])

        for td in tds:
            temp.append(sanitize(td.text))
        temp = change_types(temp)
        records.append(temp)
    return records


def fetch_news(soup, id):
    """Fetches RQuotes records from a soup object"""
    table = soup.find(id=id)
    trs = table.findAll('tr')
    if len(trs) < 2:
        return None
    trs.pop(0)
    records = []
    for tr in trs:
        tds = tr.findAll('td')

        # 1st td is expected to be something like <td>09:24:35</td>
        time = sanitize(tds.pop(0).text).split(':')
        # convert the list of strings to list of ints
        time = [int(i) for i in time]
        # return an time object
        time = datetime.time(time[0], time[1], time[2])

        # dt = datetime.datetime(2015, 4, 30)
        dt = datetime.datetime.now()

        date = datetime.datetime.combine(dt, time)

        # 2nd td is expected to be something like <td><a href='..id=..'>headline</a></td>
        a = tds.pop(0).a
        newsid = a['href'].split('=')[1]
        headline = sanitize(a.text)

        records.append([int(newsid), headline, date])
    return records


def fetch_article(soup, id):
    """Fetches single article from a soup object"""
    div = soup.find(id=id)
    if div == None:
        return None
    return div.text.strip()


def fetch_timesale(soup, id):
    """Fetches time and sale from a soup object"""
    table = soup.find(id=id)

    trs = table.findAll('tr')
    trs.pop(0)
    trs.pop(len(trs)-1)
    records = []
    for tr in trs:
        tds = tr.findAll('td')
        tds.pop(0)
        price = sanitize(tds.pop(0).text)
        price = float(price)
        quantity = sanitize(tds.pop(0).text)
        quantity = float(quantity)
        time = sanitize(tds.pop(0).text)

        # 1st td is expected to be something like <td>09:24:35</td>
        time = time.split(':')
        # convert the list of strings to list of ints
        time = [int(i) for i in time]
        # return an time object
        time = datetime.time(time[0], time[1], time[2])

        #dt = datetime.datetime(2015, 4, 30)
        dt = datetime.datetime.now()

        date = datetime.datetime.combine(dt, time)

        records.append([price, quantity, date])

    return records


def sanitize(str):
    return str.strip().replace(',', '')


def change_types(records):
    try:
        for i in [0, 6, 7]:
            records[i] = 0 if not records[i] else int(records[i])
        for i in [1, 2, 3, 4, 5, 8, 9, 10, 12, 13]:
            records[i] = 0 if not records[i] else float(records[i])

        records[11] = datetime.datetime.strptime(records[11], "%d-%m-%Y").date()
        return records
    except Exception as e:
        logging.warning(records, str(e))
    return None


def make_dict(records, names):
    listofdict = []
    for outer in records:
        dict = {}
        for i, r in enumerate(outer):
            dict[names[i]] = r
        listofdict.append(dict)
    return listofdict
