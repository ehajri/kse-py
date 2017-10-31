import unittest
import datetime
from kse.Rquotes import FetchRquotes, RquotesModel
from bs4 import BeautifulSoup


class TestFetchRquotes(unittest.TestCase):
    def setUp(self):
        self.fetch_rquotes = FetchRquotes("", "myid", MockRquotesWebReader())

    def tearDown(self):
        self.fetch_rquotes = None

    def test_should_return_appropriate_list(self):
        self.assertEqual([[123, 1.2, 0.1, 1.2, 1.3, 1.0, 100000, 20000, 213234423, 1.1, 1.2, datetime.date(2012, 12, 12), 100, 100]], self.fetch_rquotes.fetch())


class TestRquotesModel(unittest.TestCase):
    def setUp(self):
        self.fetch_rquotes = FetchRquotes("", "myid", MockRquotesWebReader())
        self.rquotes_model = RquotesModel(None, self.fetch_rquotes, "")

    def tearDown(self):
        self.fetch_rquotes = None
        self.rquotes_model = None

    def test_fetching_rquotes_is_correct(self):
        self.assertEqual(
            [[123, 1.2, 0.1, 1.2, 1.3, 1.0, 100000, 20000, 213234423, 1.1, 1.2, datetime.date(2012, 12, 12), 100, 100]],
            self.rquotes_model.fetch())

    def test_processing_rquotes_record_is_correct(self):
        pass



class MockRquotesWebReader:
    def read(self, link):
        html = """"
<table id=myid>
<tr class=header></tr>
<tr>
<td><a href='ticker.ext=123'>some text</a></td>
<td>1.2</td>
<td>0.1</td>
<td>1.2</td>
<td>1.3</td>
<td>1.0</td>
<td>100000</td>
<td>20000</td>
<td>213234423</td>
<td>1.1</td>
<td>1.2</td>
<td>12-12-2012</td>
<td>100</td>
<td>100</td>
</tr>
</table>
"""
        return BeautifulSoup(html, 'html.parser')
