# Author: Krutarth Rao
# Email: raok@purdue.edu

import sys
import unittest
import pandas
import json
from random import randint

from logging import getLogger

MOCK_LOG = getLogger()

sys.path.append('../../app/data_manager')
from parse import Parser

class TestParse(unittest.TestCase):
    '''
        JSON creation from data frame, power to energy conversion,
        query validation, data validation already tested
        in integration tests.

        TestParse tests dataframe generation. I.e. sections of the
        code that cannot be tested through integration tests.
    '''

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_parse_df_creator_valid_data(self):
        data = [
            {"datetime": "2018-08-24T00:00:00Z", "value": randint(1, 1000)},
            {"datetime": "2018-08-24T00:15:00Z", "value": randint(1, 1000)},
            {"datetime": "2018-08-24T00:30:00Z", "value": randint(1, 1000)},
        ]
        df, err = Parser.make_timeseries_df(data, MOCK_LOG)
        self.assertEqual(err, '')
        self.assertIsNotNone(df)

    def test_parse_df_creator_invalid_data_labels(self):
        data = [
            {"datetime1": "2018-08-24T00:00:00Z", "value": randint(1, 1000)},
            {"datetime2": "2018-08-24T00:15:00Z", "value": randint(1, 1000)},
            {"datetime3": "2018-08-24T00:30:00Z", "value": randint(1, 1000)},
        ]
        df, err = Parser.make_timeseries_df(data, MOCK_LOG)
        self.assertEqual(err, 'invalid labels in data object')
        self.assertIsNone(df)

    def test_parse_df_creator_negative_values(self):
        data = [
            {"datetime": "2018-08-24T00:00:00Z", "value": -1},
            {"datetime": "2018-08-24T00:15:00Z", "value": -5},
            {"datetime": "2018-08-24T00:30:00Z", "value": -20},
        ]
        df, err = Parser.make_timeseries_df(data, MOCK_LOG)
        self.assertIn('negative values in data', err)
        self.assertIsNone(df)

    def test_parse_validate_parse_valid_usage(self):
        usage_info = {
            'spaceship_id': randint(1, 100),
            'units': 'kWh',
            'data': [
                {"datetime": "2018-08-24T00:00:00Z", "value":  randint(1000, 5000)},
                {"datetime": "2018-08-24T00:15:00Z", "value": randint(1000, 5000)},
                {"datetime": "2018-08-24T00:30:00Z", "value": randint(1000, 5000)},
            ]
        }
        df, err = Parser.validate_parse_consumption_data(usage_info, MOCK_LOG)
        self.assertEqual(err, '')
        self.assertIsNotNone(df)

    def test_parse_validate_parse_missing_units_usage(self):
        usage_info = {
            'spaceship_id': randint(1, 100),
            'data': [
                {"datetime": "2018-08-24T00:00:00Z", "value":  randint(1000, 5000)},
                {"datetime": "2018-08-24T00:15:00Z", "value": randint(1000, 5000)},
                {"datetime": "2018-08-24T00:30:00Z", "value": randint(1000, 5000)},
            ]
        }
        df, err = Parser.validate_parse_consumption_data(usage_info, MOCK_LOG)
        self.assertEqual(err, 'missing units in input fields')
        self.assertIsNone(df)

    def test_parse_validate_parse_missing_data_usage(self):
        usage_info = {
            'spaceship_id': randint(1, 100),
            'units': 'kWh',
        }
        df, err = Parser.validate_parse_consumption_data(usage_info, MOCK_LOG)
        self.assertEqual(err, 'missing data in input fields')
        self.assertIsNone(df)

    def test_parse_validate_parse_empty_data_usage(self):
        usage_info = {
            'spaceship_id': randint(1, 100),
            'units': 'kWh',
            'data': []
        }
        df, err = Parser.validate_parse_consumption_data(usage_info, MOCK_LOG)
        self.assertEqual(err, 'empty data object')
        self.assertIsNone(df)




if __name__ == '__main__':
    unittest.main()