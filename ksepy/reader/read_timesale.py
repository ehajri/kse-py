from app.ksepy.common import *


def read_timesale():
    logger.info("run timesale started")
    url = config['timesale']['url2']
    dom_id = config['timesale']['dom_id2']

    s = WebReader.read(url)
    if s is None:
        logger.error("timesale couldn't read the web")
        errorlogger.error("timesale couldn't read the web")
        return
    table = s.find(id=dom_id)

    if table is None:
        logger.warning('[read_timesale] table does not exit')
        return

    trs = table.findAll('tr')

    if trs is None or len(trs) < 2:
        logger.warning('[read_timesale] table has no rows')
        return

    # first tr is headers, last is footer not needed
    trs.pop(0)
    trs.pop(len(trs) - 1)

    records = []

    for tr in trs:
        tds = tr.findAll('td')
        a = tds.pop(0).a
        ticker = a['href'].split('=')[1].split('&')[0]
        ticker = int(ticker)

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

        # dt = datetime.datetime(2015, 4, 30)
        dt = datetime.datetime.now()

        date = datetime.datetime.combine(dt, time)

        records.append([ticker, price, quantity, date])

    fields = 'ticker price quantity datetime'
    do_bulk_insert_pw(sm.Timesale, records, fields.split(' '))
    logger.info("run timesale finished")
