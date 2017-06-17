from kse.kse import *
import unittest
from bs4 import BeautifulSoup


class TestFetchOBook(unittest.TestCase):
    def setUp(self):
        self.fetch_obook = FetchOBook("", "myid", MockObookWebReader())

    def tearDown(self):
        self.fetch_obook = None

    def should_return_appropriate_list(self):
        self.assertEqual([['123', '1212', '1.2', '1000', '1.1', '50000', '']], self.fetch_obook.fetch())


class TestOBookModel(unittest.TestCase):
    def setUp(self):
        self.fetch_obook = FetchOBook("", "myid", MockObookWebReader())
        self.obook_model = OBookModel(None, self.fetch_obook, "")

    def tearDown(self):
        self.fetch_obook = None
        self.obook_model = None

    def fetching_obook_is_correct(self):
        self.assertEqual([['123', '1212', '1.2', '1000', '1.1', '50000', '']], self.obook_model.fetch())

    def processing_obook_record_is_correct(self):
        pass


class MockObookWebReader:
    def read(self, link):
        html = "<table id=myid><tr class=header></tr><tr><td><a href='ticker.ext=123&whatever'>some text</a></td><td>1212</td><td>1.2</td><td>1000</td><td>1.1</td><td>50000</td><td></td></tr></table>"
        return BeautifulSoup(html, 'html.parser')


if __name__ == '__main__':
    unittest.main()