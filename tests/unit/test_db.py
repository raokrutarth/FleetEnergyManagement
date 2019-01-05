
# Author: Krutarth Rao
# Email: raok@purdue.edu

import sys
import unittest
import pandas as pd
import numpy as np
import json
from uuid import uuid1

from logging import getLogger


sys.path.append('../../app/data_manager')
from db_ops import DBManager

MOCK_LOG = getLogger()


class TestDB(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


    def test_db_save_delete_basic(self):
        empty_db = True
        ship_id = str(uuid1())
        try:
            all_data = DBManager.dump_energy_ts(MOCK_LOG)
            db = all_data['energy']
            empty_db = False
        except KeyError:
            pass

        # create dataframe
        date_rng = pd.date_range(start='01/01/2018', end='01/04/2018', freq='15T')
        df = pd.DataFrame(date_rng, columns=['datetime'])
        df['value'] = np.random.uniform(0, 1000, size=(len(date_rng)))
        df['datetime'] = pd.to_datetime(df['datetime'])
        df = df.set_index('datetime')
        if not empty_db:
            for row in df.values:
                self.assertFalse([ship_id, row[0]] in db.values)


        # save new timeseries
        DBManager.save_energy_entry(ship_id, df)
        all_data = DBManager.dump_energy_ts(getLogger())
        db = all_data['energy']
        for row in df.values:
            self.assertTrue([ship_id, row[0]] in db.values)

        # remove ship entry
        DBManager.delete_full_energy_entry(ship_id, MOCK_LOG)
        try:
            all_data = DBManager.dump_energy_ts(getLogger())
            db = all_data['energy']
        except KeyError:
            return
        for row in df.values:
            self.assertFalse([ship_id, row[0]] in db.values)



    def test_db_save_invalid_index(self):
        ship_id = str(uuid1())
        # create invalid dataframe
        index = pd.Series(np.random.randint(100))
        df = pd.DataFrame(index, columns=['not_date'])
        df['value'] = np.random.uniform(0, 1000,size=(len(index)))
        df = df.set_index('not_date')

        with self.assertRaises(TypeError):
            # save new timeseries
            DBManager.save_energy_entry(ship_id, df)

    def test_db_query_basic(self):
        ship_id = str(uuid1())

        # create dataframe
        date_rng = pd.date_range(start='01/13/2018', end='01/15/2018', freq='15T')
        df = pd.DataFrame(date_rng, columns=['datetime'])
        df['value'] = np.random.uniform(0, 1000, size=(len(date_rng)))
        df['datetime'] = pd.to_datetime(df['datetime'])
        df = df.set_index('datetime')

        # save new timeseries
        DBManager.save_energy_entry(ship_id, df)

        # query
        start = '2018-01-13T00:00:00Z'
        end = '2018-01-15T00:00:00Z'
        got = DBManager.get_energy_entry(ship_id, start, end, MOCK_LOG)
        actual_df = got['energy']
        self.assertTrue(actual_df.equals(df))

        # remove ship entry
        DBManager.delete_full_energy_entry(ship_id, MOCK_LOG)


    def test_db_query_outofrange(self):
        ship_id = str(uuid1())

        # create dataframe
        date_rng = pd.date_range(start='01/01/2018', end='02/01/2018', freq='15T')
        df = pd.DataFrame(date_rng, columns=['datetime'])
        df['value'] = np.random.uniform(0, 1000, size=(len(date_rng)))
        df['datetime'] = pd.to_datetime(df['datetime'])
        df = df.set_index('datetime')

        # save new timeseries
        DBManager.save_energy_entry(ship_id, df)

        # query
        start = '2019-01-01T00:00:00Z'
        end = '2022-01-05T00:00:00Z'
        got = DBManager.get_energy_entry(ship_id, start, end, MOCK_LOG)
        self.assertTrue(not got)

        # remove ship entry
        DBManager.delete_full_energy_entry(ship_id, MOCK_LOG)

if __name__ == '__main__':
    unittest.main()
