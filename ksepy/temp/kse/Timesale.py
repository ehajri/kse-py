from kse.kse import MyBaseModel
from kse import stock_models as sm
import datetime
from kse import func, kse


class FetchTimesale:
    def __init__(self, url, domId, web_reader):
        self.url = url
        self.domId = domId
        self.web_reader = web_reader

    def fetch(self):
        page_content = self.web_reader.read(self.url)
        return self._fetch_timesale(page_content, self.domId)

    def _fetch_timesale(self, soup, id):
        """Fetches time and sale from a soup object"""
        table = soup.find(id=id)

        if table is None:
            return None

        trs = table.findAll('tr')

        if trs is None or len(trs) == 1:
            return None

        trs.pop(0)
        trs.pop(len(trs) - 1)
        records = []
        for tr in trs:
            tds = tr.findAll('td')
            a = tds.pop(0).a
            ticker = a['href'].split('=')[1].split('&')[0]
            ticker = int(ticker)

            price = func.sanitize(tds.pop(0).text)
            price = float(price)
            quantity = func.sanitize(tds.pop(0).text)
            quantity = float(quantity)
            time = func.sanitize(tds.pop(0).text)

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

        return records


class TimesaleModel(MyBaseModel):
    def __init__(self, running_model: sm.Timesale, fetch_timesale, repo):
        super().__init__()
        self.fields = 'ticker_id price quantity datetime'
        self.running_model = running_model
        self.fetch_timesale = fetch_timesale
        self.repo = repo

    def fetch(self):
        return self.fetch_timesale.fetch()

    def process(self, records):
        kse.logger.info("%s TimeSale Listener started!" % datetime.datetime.now().time())

        if records is None:
            kse.logger.warning("Nothing returned from FetchTimeSale2")
        elif len(list) == 0:
            kse.logger.warning("0 record returned from FetchTimeSale2")
        else:
            return records
        return None

    def save(self, records):
        kse.logger.info('Timesale.save is called for %s records.', len(records))
        kse.do_individual_insert_pw(sm.Timesale, records, self.fields.split(' '))
        # self.repo.insert(records, self.fields.split(' '))

    def execute(self):
        kse.logger.debug('executing')
        records = self.fetch()
        records = self.process(records)
        self.save(records)
