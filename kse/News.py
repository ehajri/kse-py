from kse.kse import MyBaseModel
from kse import stock_models as sm
import datetime
from kse import func, kse


class FetchNews:
    def __init__(self, url, domId, web_reader):
        self.url = url
        self.domId = domId
        self.web_reader = web_reader

    def fetch(self):
        page_content = self.web_reader.read(self.url)
        return self._fetch_news(page_content, self.domId)

    def _fetch_news(self, soup, id):
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
            time = func.sanitize(tds.pop(0).text).split(':')
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
            headline = func.sanitize(a.text)

            records.append([int(newsid), headline, date])
        return records

class NewsModel(MyBaseModel):
    def __init__(self, running_model: sm.News, fetch_news, repo):
        super().__init()
        self.field = ''
        self.running_model = running_model
        self.fetch_news = fetch_news
        self.repo = repo

    def fetch(self):
        return self.fetch_news.fetch()

    def process(self, records):
        pass

    def save(self, records):
        pass

    def execute(self):
        pass