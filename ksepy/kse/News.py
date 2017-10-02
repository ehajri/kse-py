from kse.kse import MyBaseModel
from kse import stock_models as sm
import datetime
from kse import func, kse


class FetchNews:
    def __init__(self, url, domId, url2, domId2,  web_reader):
        self.url = url
        self.domId = domId
        self.url2 = url2
        self.domId2 = domId2
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

    def fetch2(self):
        pass

    def _fetch_news2(self, soup, id):
        pass


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
        kse.logger.info("%s News Listener started!" % datetime.datetime.now().time())

        if records is None:
            kse.logger.warning("News did not return anything")
            return

        for i in records:
            if self._is_existed(i[0], i[2]):
                records.remove(i)

        for i in records:
            i[2] = i[2].strftime('%Y-%m-%d %H:%M:%S')
            # i[0] is the id for the news

            temp = self.fetch_news.fetch2()

            if temp is None or temp == '':
                kse.logger.warning("%d returned none" % i[0])
                i.append('')
            else:
                # print("%d to insert" % i[0])
                i.append(temp)
        return records

    def _is_existed(article_id, article_date):
        count = sm.db.News.select().where(sm.db.News.id == article_id and sm.db.News.date == article_date).count()
        return count > 0

    def save(self, records):
        # do_insert_news(records, fields)
        kse.do_bulk_insert_pw(sm.db.News, records, self.fields.split(' '))

    def execute(self):
        pass