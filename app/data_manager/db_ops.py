from influxdb import DataFrameClient
import os
import requests
import time
import pandas as pd




DB_HOST = os.getenv('INFLUX_HOST', 'localhost')
DB_PORT = os.getenv('INFLUX_PORT', '8086')
DB_UNAME = os.getenv('INFLUX_USER', 'root')
DB_PWD = os.getenv('INFLUX_PASS', 'root')
DB_DBNAME = os.getenv('INFLUX_DBNAME', 'energy_service')

DB_CLIENT = DataFrameClient(
                host=DB_HOST,
                port=DB_PORT,
                username=DB_UNAME,
                password=DB_PWD,
                database=DB_DBNAME
            )

TIMESERIES_NAME = 'energy'
TAG_KEY = 'ship_id'

class DBManager:
    '''
        Database client for influxDB
    '''
    @staticmethod
    def test_connection(log):
        is_connected = False
        while not is_connected:
            log.debug('[{} {} {} {}]Trying InfluxDB connection...'.format(
                DB_HOST,
                DB_PORT,
                DB_UNAME,
                DB_PWD
            ))
            try:
                log.debug('Connection successful. Existing dbs: {}'.format(
                    DB_CLIENT.get_list_database())
                )
            except requests.exceptions.ConnectionError:
                log.warning('No InfluxDB connection yet. Waiting 5 seconds and '+
                    'retrying.')
                time.sleep(5)
            else:
                is_connected = True


    @staticmethod
    def dump_energy_ts(log):
        return DB_CLIENT.query('SELECT * FROM {}'.format(TIMESERIES_NAME))

    @staticmethod
    def save_energy_entry(ship_id, timeseries):
        return DB_CLIENT.write_points(
            timeseries,
            measurement=TIMESERIES_NAME,
            tags={TAG_KEY: str(ship_id)},
            protocol='json')

    @staticmethod
    def get_full_energy_entry(ship_id):
        return DB_CLIENT.query("SELECT * FROM {} WHERE {}='{}'".format(
                    TIMESERIES_NAME,
                    TAG_KEY,
                    str(ship_id)
                    )
                )
    @staticmethod
    def get_energy_entry(ship_id, start, end, log):
        log.debug('Making DB time query. ship_id: {}, start: {}, end: {}'.format(
            ship_id, start, end))
        start = pd.Timestamp(start)
        end = pd.Timestamp(end)
        return DB_CLIENT.query(
            ("SELECT * FROM {} WHERE {}='{}' AND time >= '{}' AND time <= '{}'").format(
                TIMESERIES_NAME,
                TAG_KEY,
                str(ship_id),
                start.isoformat(),
                end.isoformat())
            )

    @staticmethod
    def delete_full_energy_entry(ship_id, log):
        log.debug('Deleting DB entry for ship_id: {}'.format(ship_id))
        return DB_CLIENT.query(
            ("DELETE FROM {} WHERE {}='{}'").format(
                TIMESERIES_NAME,
                TAG_KEY,
                str(ship_id),
            ))

    @staticmethod
    def delete_all_data(log):
        log.critical('Deleting all DB entries')
        return DB_CLIENT.query(
            ("DELETE FROM {}").format(
                TIMESERIES_NAME,
            ))

