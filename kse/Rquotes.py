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