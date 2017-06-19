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
        pass

class MockNewsWebReader:
    pass