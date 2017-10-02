from kse.kse import *
import unittest
from bs4 import BeautifulSoup
from datetime import datetime
from kse.News import NewsModel, FetchNews


class TestFetchNews(unittest.TestCase):
    def setUp(self):
        self.fetch_news = FetchNews("","myid", MockNewsWebReader())

    def tearDown(self):
        self.fetch_news = None

    def test_should_return_appropriate_list(self):
        dt = datetime.today().replace(hour=9, minute=24, second=35, microsecond=0)
        self.assertEqual([[123, 'some text', dt]], self.fetch_news.fetch())

class MockNewsWebReader:
    def read(self, link):
        html = """
<table id=myid>
<tr class=header>
</tr>
<tr>
<td>09:24:35</td>
<td><a href='news.ext=123'>some text</a></td>
</tr>
</table>
"""
        return BeautifulSoup(html, 'html.parser')