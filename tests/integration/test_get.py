

import requests
import unittest
import sys
import json
from http import HTTPStatus
from logging import getLogger

from mock_data import *
sys.path.append('../../app/data_manager')
from db_ops import DBManager


HOST_URL = 'http://127.0.0.1:5000/data'


class TestGet(unittest.TestCase):

    # tests assume the timestamps are in ascending order
    to_post = [BASIC, TO_AGG, TO_DISSAGG, TO_CONV, TO_CONV_AGG, TO_CONV_DISAGG, TO_CONV_MIXED]
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        for data in cls.to_post:
            resp = requests.post(url=HOST_URL, json=data)
            expected = 'Data saved successfully for ship'
            if (expected not in  resp.text) or (resp.status_code != HTTPStatus.OK):
                raise AssertionError

    @classmethod
    def tearDownClass(cls):
        for data in cls.to_post:
            DBManager.delete_full_energy_entry(data['spaceship_id'], getLogger())

    def test_get_basic(self):
        expected_raw = {
            "spaceship_id": BASIC['spaceship_id'],
            "units": 'kWh',
            "data": BASIC['data']
        }
        params = {
            'spaceship_id': BASIC['spaceship_id'],
            'start': BASIC['data'][0]['datetime'],
            'end': BASIC['data'][-1]['datetime'],
        }
        resp = requests.get(url=HOST_URL, params=params)
        expected = json.dumps(expected_raw, sort_keys=True)
        actual = json.dumps(resp.json(), sort_keys=True)
        self.assertEqual(actual, expected)
        self.assertEqual(resp.status_code, HTTPStatus.OK)

    def test_get_basic_selected_time(self):
        expected_raw = {
            "spaceship_id": BASIC['spaceship_id'],
            "units": 'kWh',
            "data": BASIC['data'][1:-1]
        }
        params = {
            'spaceship_id': BASIC['spaceship_id'],
            'start': BASIC['data'][1]['datetime'],
            'end': BASIC['data'][-2]['datetime'],
        }
        resp = requests.get(url=HOST_URL, params=params)
        expected = json.dumps(expected_raw, sort_keys=True)
        actual = json.dumps(resp.json(), sort_keys=True)
        self.assertEqual(actual, expected)
        self.assertEqual(resp.status_code, HTTPStatus.OK)

    def test_get_basic_outofrange_time(self):
        params = {
            'spaceship_id': BASIC['spaceship_id'],
            'start':"2028-08-24T04:15:00Z",
            'end': "2038-08-24T04:15:00Z",
        }
        resp = requests.get(url=HOST_URL, params=params)
        expected = 'No entries found in date range'
        actual = json.dumps(resp.json(), sort_keys=True)
        self.assertIn(expected, actual)
        self.assertEqual(resp.status_code, HTTPStatus.BAD_REQUEST)

    def test_get_basic_invalid_time(self):
        params = {
            'spaceship_id': BASIC['spaceship_id'],
            'start':"2018-99-24T04:15:00Z",
            'end': "2018-08-35T04:15:00Z",
        }
        resp = requests.get(url=HOST_URL, params=params)
        expected1 = 'invalid start'
        expected2 = 'invalid end'
        actual = json.dumps(resp.json(), sort_keys=True)
        self.assertIn(expected1, actual)
        self.assertIn(expected2, actual)
        self.assertEqual(resp.status_code, HTTPStatus.BAD_REQUEST)

    def test_get_basic_missing_id(self):
        params = {
            'start':"2018-99-24T04:15:00Z",
            'end': "2018-08-35T04:15:00Z",
        }
        resp = requests.get(url=HOST_URL, params=params)
        expected = 'spaceship_id not found'
        actual = json.dumps(resp.json(), sort_keys=True)
        self.assertIn(expected, actual)
        self.assertEqual(resp.status_code, HTTPStatus.BAD_REQUEST)

    def test_get_agg(self):
        expected_raw = {
            "spaceship_id": TO_AGG['spaceship_id'],
            "units": 'kWh',
            "data": [
                {"datetime": "2018-08-24T04:15:00Z", "value": 9}
            ]
        }
        params = {
            'spaceship_id': TO_AGG['spaceship_id'],
            'start': '2018-08-24T04:00:00Z',
            'end': '2018-08-24T04:15:00Z',
        }
        resp = requests.get(url=HOST_URL, params=params)
        expected = json.dumps(expected_raw, sort_keys=True)
        actual = json.dumps(resp.json(), sort_keys=True)
        self.assertEqual(actual, expected)

    def test_get_disagg(self):
        expected_raw = {
            "spaceship_id": TO_DISSAGG['spaceship_id'],
            "units": 'kWh',
            "data": [
                {"datetime": "2019-01-01T04:15:00Z", "value": 2},
                {"datetime": "2019-01-01T04:30:00Z", "value": 0},
                {"datetime": "2019-01-01T04:45:00Z", "value": 1},
                {"datetime": "2019-01-01T05:00:00Z", "value": 0},
            ]
        }
        params = {
            'spaceship_id': TO_DISSAGG['spaceship_id'],
            'start': TO_DISSAGG['data'][0]['datetime'],
            'end': '2019-01-01T05:10:01Z',
        }
        resp = requests.get(url=HOST_URL, params=params)
        expected = json.dumps(expected_raw, sort_keys=True)
        actual = json.dumps(resp.json(), sort_keys=True)
        self.assertEqual(actual, expected)

    def test_get_toconvert(self):
        expected_raw = {
            "spaceship_id": TO_CONV['spaceship_id'],
            "units": 'kWh',
            "data": [
                {"datetime": "2006-12-24T04:00:00Z", "value": 57},
                {"datetime": "2006-12-24T04:15:00Z", "value": 30},
                {"datetime": "2006-12-24T04:30:00Z", "value": 162},
            ]
        }
        params = {
            'spaceship_id': TO_CONV['spaceship_id'],
            'start': TO_CONV['data'][0]['datetime'],
            'end': TO_CONV['data'][-1]['datetime'],
        }
        resp = requests.get(url=HOST_URL, params=params)
        expected = json.dumps(expected_raw, sort_keys=True)
        actual = json.dumps(resp.json(), sort_keys=True)
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
