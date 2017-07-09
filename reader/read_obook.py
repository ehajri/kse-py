from common import *


def read_obook():
    logger.info("run obook started")
    url = config['obook']['url']
    dom_id = config['obook']['dom_id']

    s = WebReader.read(url)
    table = s.find(id=dom_id)

    if table is None:
        logger.warning('[read_obook] table does not exit')
        return

    trs = table.findAll('tr')

    if trs is None or len(trs) < 2:
        logger.warning('[read_obook] table has no rows')
        return None

    # first tr is headers, not needed
    trs.pop(0)

    records = []

    for tr in trs:
        temp = []
        tds = tr.findAll('td')
        a = tds.pop(0).a
        ticker = a['href'].split('=')[1].split('&')[0]
        temp.append(ticker)

        # append rest of tds
        for td in tds:
            temp.append(sanitize(td.text))
        temp.append(datetime.datetime.today().date())
        records.append(temp)


    fields = 'ticker price bid bid_qty ask ask_qty createdon'
    do_bulk_insert_pw(sm.Obook, records, fields.split(' '))
    logger.info("run obook finished")
