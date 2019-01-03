

import requests
import unittest
import sys
import json
from http import HTTPStatus
from random import randint
from logging import getLogger

from uuid import uuid1

sys.path.append('../../app/data_manager')
from db_ops import DBManager

HOST_URL = 'http://127.0.0.1:5000/data'



class TestPost(unittest.TestCase):

    def test_post_response_basic(self):
        ship_id = str(uuid1())
        data = {
            "spaceship_id": ship_id,
            "units": "kWh",
            "data": [
                {
                    "datetime": "2018-08-24T00:00:00Z",
                    "value": randint(0, 500)
                },
                {
                    "datetime": "2018-08-24T01:00:00Z",
                    "value": randint(0, 500)
                },
                {
                    "datetime": "2018-08-24T02:00:00Z",
                    "value": randint(0, 500)
                }
            ]
        }
        resp = requests.post(url=HOST_URL, json=data)
        expected = 'Data saved successfully for ship %s' % ship_id
        self.assertEqual(resp.text, expected)
        DBManager.delete_full_energy_entry(ship_id, getLogger())

    def test_post_response_missing_units_label(self):
        ship_id = str(uuid1())
        data = {
            "spaceship_id": ship_id,
            "data": [
                {
                    "datetime": "2018-08-24T00:00:00Z",
                    "value": randint(0, 500)
                },
                {
                    "datetime": "2018-08-24T01:00:00Z",
                    "value": randint(0, 500)
                },
                {
                    "datetime": "2018-08-24T02:00:00Z",
                    "value": randint(0, 500)
                }
            ]
        }
        resp = requests.post(url=HOST_URL, json=data)
        expected = 'missing units in input fields'
        self.assertEqual(resp.text, expected)
        self.assertEqual(resp.status_code, HTTPStatus.BAD_REQUEST)
        DBManager.delete_full_energy_entry(ship_id, getLogger())

    def test_post_response_empty_data(self):

        ship_id = str(uuid1())
        data = {
            "spaceship_id": ship_id,
            "units": "kWh",
            "data": []
        }
        resp = requests.post(url=HOST_URL, json=data)
        expected = 'empty data object'
        self.assertIn(expected, resp.text)
        self.assertEqual(resp.status_code, HTTPStatus.BAD_REQUEST)
        DBManager.delete_full_energy_entry(ship_id, getLogger())

    def test_post_invalid_units(self):
        ship_id = str(uuid1())
        data = {
            "spaceship_id": ship_id,
            "units": "kiloWattHour",
            "data": [
                {
                    "datetime": "2018-08-24T00:00:00Z",
                    "value": randint(0, 500)
                },
            ]
        }
        resp = requests.post(url=HOST_URL, json=data)
        expected = 'invalid units'
        self.assertIn(expected, resp.text)
        self.assertEqual(resp.status_code, HTTPStatus.BAD_REQUEST)
        DBManager.delete_full_energy_entry(ship_id, getLogger())

    def test_post_negative_values(self):
        ship_id = str(uuid1())
        data = {
            "spaceship_id": ship_id,
            "units": "kWh",
            "data": [
                {
                    "datetime": "2018-08-24T04:00:00Z",
                    "value": randint(0, 500)
                },
                {
                    "datetime": "2018-08-24T04:01:00Z",
                    "value": randint(0, 500)
                },
                {
                    "datetime": "2018-08-25T04:00:00Z",
                    "value": -100
                },
                {
                    "datetime": "2018-08-25T04:01:00Z",
                    "value": -1
                },
            ]
        }
        resp = requests.post(url=HOST_URL, json=data)
        expected = 'negative values'
        self.assertIn(expected, resp.text)
        self.assertEqual(resp.status_code, HTTPStatus.BAD_REQUEST)
        DBManager.delete_full_energy_entry(ship_id, getLogger())

    def test_post_duplicate_timestamps(self):
        ship_id = str(uuid1())
        data = {
            "spaceship_id": ship_id,
            "units": "kWh",
            "data": [
                {
                    "datetime": "2018-08-24T04:00:00Z",
                    "value": randint(0, 500)
                },
                {
                    "datetime": "2018-08-24T04:00:00Z",
                    "value": randint(0, 500)
                },
            ]
        }
        resp = requests.post(url=HOST_URL, json=data)
        expected = 'duplicate timestamps'
        self.assertIn(expected, resp.text)
        self.assertEqual(resp.status_code, HTTPStatus.BAD_REQUEST)
        DBManager.delete_full_energy_entry(ship_id, getLogger())

    def test_post_invalid_timestamps(self):
        ship_id = str(uuid1())
        data = {
            "spaceship_id": ship_id,
            "units": "kWh",
            "data": [
                {
                    "datetime": "2018-08-34T04:00:00Z",
                    "value": randint(0, 500)
                },
                {
                    "datetime": "2018-09-24T99:99:00Z",
                    "value": randint(0, 500)
                },
            ]
        }
        resp = requests.post(url=HOST_URL, json=data)
        expected = 'invalid data object'
        self.assertIn(expected, resp.text)
        self.assertEqual(resp.status_code, HTTPStatus.BAD_REQUEST)
        DBManager.delete_full_energy_entry(ship_id, getLogger())

    def test_post_missing_data_value(self):
        ship_id = str(uuid1())
        data = {
            "spaceship_id": ship_id,
            "units": "kWh",
            "data": [
                {
                    "datetime": "2018-09-24T04:00:00Z",
                },
                {
                    "datetime": "2018-09-24T02:12:00Z",
                    "value": randint(0, 500)
                },
            ]
        }
        resp = requests.post(url=HOST_URL, json=data)
        expected = 'Data saved successfully for ship'
        self.assertIn(expected, resp.text)
        self.assertEqual(resp.status_code, HTTPStatus.OK)
        DBManager.delete_full_energy_entry(ship_id, getLogger())

    def test_post_missing_data_timestamp(self):
        ship_id = str(uuid1())
        data = {
            "spaceship_id": ship_id,
            "units": "kWh",
            "data": [
                {
                    "value": randint(0, 500)
                },
                {
                    "datetime": "2018-09-24T01:45:00Z",
                    "value": randint(0, 500)
                },
            ]
        }
        resp = requests.post(url=HOST_URL, json=data)
        expected = 'Data saved successfully for ship'
        self.assertIn(expected, resp.text)
        self.assertEqual(resp.status_code, HTTPStatus.OK)
        DBManager.delete_full_energy_entry(ship_id, getLogger())




    # def test_post_missing_keys():
    #     a, b = json.dumps(a, sort_keys=True), json.dumps(b, sort_keys=True)
    #     a == b

if __name__ == '__main__':
    unittest.main()
