from kse.kse import MyBaseModel
from kse import stock_models as sm
import datetime
from kse import func, kse


class FetchRquotes:
    def __init__(self, url, domId, web_reader):
        self.url = url
        self.domId = domId
        self.web_reader = web_reader

    def fetch(self):
        page_content = self.web_reader.read(self.url)
        return self._fetch_rquotes(page_content, self.domId)

    def _fetch_rquotes(self, soup, id):
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
                temp.append(func.sanitize(td.text))
            temp = func.change_types(temp)
            records.append(temp)
        return records


class RquotesModel(MyBaseModel):
    def __init__(self, running_model: sm.Rquotes, fetch_rquotes, repo):
        super().__init__()
        self.fields = 'ticker_id last change open high low vol trade value prev ref prev_date bid ask'
        self.running_model = running_model
        self.fetch_rquotes = fetch_rquotes
        self.repo = repo

    def fetch(self):
        return self.fetch_rquotes.fetch()

    def process(self, records):
        kse.logger.info("%s TimeSale Listener started!" % datetime.datetime.now().time())

        if records is None:
            kse.logger.warning("Nothing returned from FetchRQuotes")
            return None
        else:
            # list.append([507, 108.000, 8.000, 108.000, 108.000, 108.000, 1, 2, 108.000, 100.000, 100.000, '2017-04-15', 96.000, 0.000]);
            records = [x for x in records if all(xx != 0 for xx in x[1:9])]
            return records

    def save(self, records):
        kse.logger.info('Rquotes.save is called for %s records.', len(records))
        kse.do_bulk_insert_pw(sm.Rquotes, records, self.fields.split(' '))

    def execute(self):
        kse.logger.debug('executing')
        records = self.fetch()
        records = self.process(records)
        self.save(records)
