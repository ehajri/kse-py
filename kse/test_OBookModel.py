from unittest import TestCase
from kse import OBook


class TestOBookModel(TestCase):
    def setUp(self):
        self.fetch_obook = MockFetchOBook()
        self.obook_model = kse.OBookModel(None, self.fetch_obook)

    def fetching_obook_is_correct(self):
        self.assertEqual(self.obook_model.fetch(), "<html></html>")

    def tearDown(self):
        self.fetch_obook = None
        self.obook_model = None


class MockFetchOBook:
    def fetch(self):
        return "<html></html>"
