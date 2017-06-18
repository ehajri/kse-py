from kse.kse import MyBaseModel
from kse import stock_models as sm
from datetime import datetime
from kse import func, kse


class FetchOBook:
    def __init__(self, url, domId, web_reader):
        self.url = url
        self.domId = domId
        self.web_reader = web_reader

    def fetch(self):
        page_content = self.web_reader.read(self.url)
        return self._fetch_obook(page_content, self.domId)

    def _fetch_obook(self, soup, id):
        """Fetches Orders Book from a soup object"""
        table = soup.find(id=id)

        if table is None:
            return None
        # print(table)
        trs = table.findAll('tr')
        if trs is None:
            return None
        # print(trs)
        trs.pop(0)
        records = []
        for tr in trs:
            temp = []
            # 1st td has the ticker id, so let's fetch it
            tds = tr.findAll('td')
            a = tds.pop(0).a
            ticker = a['href'].split('=')[1].split('&')[0]
            temp.append(ticker)

            # get the rest of the tds
            for td in tds:
                temp.append(func.sanitize(td.text))
            records.append(temp)
        return records


class OBookModel(MyBaseModel):
    def __init__(self, running_model: sm.Running, fetch_obook, repo):
        super().__init__()
        self.fields = 'ticker price bid bid_qty ask ask_qty createdon'
        self.running_model = running_model
        self.fetch_obook = fetch_obook
        self.repo = repo

    def fetch(self):
        return self.fetch_obook.fetch()

    def process(self, records):
        if records is None:
            kse.logger.warning('OBook.process: no record passed')
            return

        for i, a in enumerate(records):
            # cleaning the records, and appending date at end of the record
            records[i] = [(float(x) if x else 0) for x in a]
            records[i].append(datetime.datetime.today().date())

        return records

    def save(self, records):
        kse.logger.debug('OBook.save is called for %s records.', len(records))
        kse.do_individual_insert_pw(sm.Obook, records, self.fields.split(' '))
        # self.repo.insert(records, self.fields.split(' '))

    def execute(self):
        kse.logger.debug('executing')
        records = self.fetch()
        records = self.process(records)
        self.save(records)
