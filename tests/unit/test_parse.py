
import sys
import unittest
import pandas
import json

sys.path.append('../../app/data_manager')
from parse import Parser

class TestParse(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_parse_db_obj_converter(self):
        pass

    def test_parse_query_validator(self):
        pass

    def test_parse_power_df_converter(self):
        pass

    def test_parse_energy_df_converter(self):
        pass

    def test_parse_timeseries_df_creator(self):
        pass

if __name__ == '__main__':
    unittest.main()