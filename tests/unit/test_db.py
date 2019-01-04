
import sys
import unittest
import pandas
import json


sys.path.append('../../app/data_manager')
from db_ops import DBManager


class TestDB(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_save_basic(self):

        pass

    def test_save_invalid(self):

        pass

    def test_query_basic(self):

        pass

    def test_query_outofrange(self):

        pass

    def test_query_larger_range(self):

        pass

if __name__ == '__main__':
    unittest.main()
