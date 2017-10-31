from app.ksepy.common import *


def read_rquotes():
    logger.info("run rquotes started")
    url = config['rquotes']['url']
    dom_id = config['rquotes']['dom_id']

    s = WebReader.read(url)
    if s is None:
        logger.error("rquotes couldn't read the web")
        errorlogger.error("rquotes couldn't read the web")
        return

    table = s.find(id=dom_id)

    if table is None:
        logger.warning('[read_rquotes] table does not exit')
        return

    trs = table.findAll('tr')

    if trs is None or len(trs) < 2:
        logger.warning('[read_rquotes] table has no rows')
        return

    # first tr is headers, not needed
    trs.pop(0)

    records = []

    for tr in trs:
        temp = []
        tds = tr.findAll('td')

        td = tds.pop(0)

        ticker = td.text

        # removing unwanted td with ticker name
        tds.pop(0)

        temp.append(ticker)

        # append rest of tds
        for td in tds:
            temp.append(sanitize(td.text))
        temp = change_types(temp)
        records.append(temp)

    fields = 'ticker last change open high low vol trade value prev ref prev_date bid ask'
    do_bulk_insert_pw(sm.Rquotes, records, fields.split(' '))
    logger.info("run rquotes finished")