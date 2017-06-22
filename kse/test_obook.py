from kse.kse import *
import unittest
from bs4 import BeautifulSoup
from datetime import datetime
from kse.Obook import ObookModel, FetchObook


class TestFetchObook(unittest.TestCase):
    def setUp(self):
        self.fetch_obook = FetchObook("", "myid", MockObookWebReader())

    def tearDown(self):
        self.fetch_obook = None

    def test_should_return_appropriate_list(self):
        self.assertEqual([['123', '1212', '1.2', '1000', '1.1', '50000', '']], self.fetch_obook.fetch())


class TestOBookModel(unittest.TestCase):
    def setUp(self):
        self.fetch_obook = FetchObook("", "myid", MockObookWebReader())
        self.obook_model = ObookModel(self.fetch_obook, MockObookRepository())

    def tearDown(self):
        self.fetch_obook = None
        self.obook_model = None

    def test_fetching_obook_is_correct(self):
        self.assertEqual([['123', '1212', '1.2', '1000', '1.1', '50000', '']], self.obook_model.fetch())

    def test_processing_obook_record_is_correct(self):
        records = self.obook_model.fetch()
        p = self.obook_model.process(records)[0]

        self.assertEqual(123, p[0])
        self.assertEqual(1212, p[1])
        self.assertEqual(1.2, p[2])
        self.assertEqual(1000, p[3])
        self.assertEqual(1.1, p[4])
        self.assertEqual(50000, p[5])
        self.assertEqual(datetime.today().date(), p[7])

    def test_executing_obook(self):
        self.obook_model.execute()


class MockObookWebReader:
    def read(self, link):
        html = "<table id=myid><tr class=header></tr><tr><td><a href='ticker.ext=123&whatever'>some text</a></td><td>1212</td><td>1.2</td><td>1000</td><td>1.1</td><td>50000</td><td></td></tr></table>"
        return BeautifulSoup(html, 'html.parser')


class MockObookRepository:
    def __init__(self):
        self._repo = []

    def insert(self, item):
        pass
    def insert_many(self, items):
        pass

    def get(self, id):
        for item in self._repo:
            if item.id == id:
                return item
        return None
