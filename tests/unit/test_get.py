

import requests
import unittest
import sys
import json
from http import HTTPStatus
from logging import getLogger

from test_data import *
sys.path.append('../../app/data_manager')
from db_ops import DBManager


HOST_URL = 'http://127.0.0.1:5000/data'


class TestGet(unittest.TestCase):

    # tests assume the timestamps are in ascending order
    to_post = [BASIC, TO_AGG, TO_DISSAGG, TO_CONV, TO_CONV_AGG, TO_CONV_DISAGG, TO_CONV_MIXED]

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


if __name__ == '__main__':
    unittest.main()
