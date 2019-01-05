
import sys
import unittest
import pandas
import json

sys.path.append('../../app/data_manager')
from parse import Parser

class TestParse(unittest.TestCase):
    '''
        Dataframe generation, JSON creation
        from data frame, power to energy conversion,
        query validation, data validation already tested
        in integration tests.
    '''

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':
    unittest.main()