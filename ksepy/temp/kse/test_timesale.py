import unittest
from kse.Timesale import FetchTimesale, TimesaleModel

from bs4 import BeautifulSoup
import datetime

class TestFetchTimesale(unittest.TestCase):
    def setUp(self):
        self.fetch_timesale = FetchTimesale("", "myid", MockTimesaleWebReader())

    def tearDown(self):
        self.fetch_timesale = None

    def test_should_return_appropriate_list(self):
        self.assertEqual([[123, 1.2, 1000, datetime.datetime.today().replace(hour=9, minute=24, second=35, microsecond=0)]], self.fetch_timesale.fetch())


class MockTimesaleWebReader:
    def read(self, link):
        html = "<table id=myid><tr class=header></tr><tr><td><a href='ticker.ext=123&whatever'>some text</a></td><td>1.2</td><td>1000</td><td>09:24:35</td></tr><tr class=footer></tr></table>"
        return BeautifulSoup(html, 'html.parser')


class TestTimesaleModel(unittest.TestCase):
    def setUp(self):
        self.fetch_timesale = FetchTimesale("", "myid", MockTimesaleWebReader())
        self.timesale_model = TimesaleModel(None, self.fetch_timesale, "")

    def tearDown(self):
        self.fetch_timesale = None
        self.timesale_model = None

    def test_fetching_timesale_is_correct(self):
        self.assertEqual([['123', '1212', '1.2', '1000', '1.1', '50000', '']], self.timesale_model.fetch())

    def test_processing_timesale_record_is_correct(self):
        records = self.timesale_model.fetch()
        p = self.timesale_model.process(records)[0]

        self.assertEqual(123, p[0])
        self.assertEqual(1212, p[1])
        self.assertEqual(1.2, p[2])
        self.assertEqual(1000, p[3])
        self.assertEqual(1.1, p[4])
        self.assertEqual(50000, p[5])
        self.assertEqual(datetime.today().date(), p[7])