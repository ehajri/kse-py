#from unittest import TestCase
from kse.kse import *

import unittest


class TestOBookModel(unittest.TestCase):
    def setUp(self):
        self.fetch_obook = MockFetchOBook()
        self.obook_model = OBookModel(None, self.fetch_obook)

    def tearDown(self):
        self.fetch_obook = None
        self.obook_model = None

    def fetching_obook_is_correct(self):
        self.assertEqual(self.obook_model.fetch(), "<html></html>")

    def processing_obook_record_is_correct(self):




class MockFetchOBook:
    def fetch(self):
        return "<html></html>"


if __name__ == '__main__':
    unittest.main()