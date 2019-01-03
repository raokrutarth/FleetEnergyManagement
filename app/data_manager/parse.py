

from datetime import datetime
import dateutil.parser as dateparser
import pandas as pd
import numpy as np
import json


TIME_FREQ = '15T' # 15 mins
OUTER_KEYS = set(["spaceship_id", "units", "data"])
UNITS = set(['kw', 'kwh'])
COLUMNS = set(['datetime', 'value'])


class Parser:

    @staticmethod
    def make_timeseries_df(data, log):
        try:
            df = pd.DataFrame(data)
            if len(df) == 0:
                return None, 'empty data object'
            if not COLUMNS.issubset(df.columns):
                # verify each time event has the required labels
                log.debug('invalid labels in data object. \nexpected: {}\ngot: {}'.format(COLUMNS, df.columns))
                return None, 'invalid labels in data object'
            if any(df['value'] < 0):
                return None, 'got negative values in data. Negative power/energy usage not allowed'
            df['datetime'] = pd.to_datetime(df['datetime'], utc=True)
            df['value'] = df['value'].astype('float')

            if df['datetime'].isnull().any().any():
                log.error('missing timestamp for a datapoint in {}'.format(data))
            if df['value'].isnull().any().any():
                log.error('missing value for a datapoint in {}'.format(data))

            df.dropna(inplace=True)
            df = df.set_index('datetime')
            df = df.sort_index()

            if not pd.Series(df.index).is_unique:
                return None, 'duplicate timestamps detected in energy/power usage data'
            log.info('Timeseries dataframe created for {}'.format(data))
            return df, ''
        except ValueError:
            log.debug('Invalid values in "data" object detected: {}'.format(data))
            return None, 'invalid data object'
        except KeyError:
            log.debug('Invalid/missing labels in data object detected: {}'.format(data))
            return None, 'invalid data object'
        except Exception as e:
            log.error('Unknown error parsing data object: {}'.format(data))
            log.error(e)
            return None, 'unknown error parsing data object'


    @staticmethod
    def validate_parse_consumption_data(consumption_info, log):
        if not consumption_info:
            return None, 'missing json object in request'

        for label in OUTER_KEYS:
            if label not in consumption_info:
                return None, "missing {} in input fields".format(label)

        if consumption_info['units'].lower() not in UNITS:
            return None, 'invalid units {}'.format(consumption_info['units'])

        return Parser.make_timeseries_df(consumption_info['data'], log)

    @staticmethod
    def split(energy_usage_df, logger):
        '''
            splits an energy timeseries to a 15-min interval
            timeseries

            TODO verify disaggregation & aggregation timestamps
        '''
        grouped = energy_usage_df.groupby(pd.Grouper(freq=TIME_FREQ, label='right')).sum()
        # keep original data if already 15-min spaced
        if len(grouped) != len(energy_usage_df):
            energy_usage_df = grouped
        logger.debug('After split: {}'.format(energy_usage_df))
        return energy_usage_df, ''

    @staticmethod
    def convert_and_split(power_usage_df, logger):
        '''
            Converts kW data to kWh

            TODO verify conversion
        '''
        grouped = power_usage_df.groupby(pd.Grouper(freq=TIME_FREQ, label='right')).mean()
        # Don't change the labels if already 15min spaced
        if len(grouped) != len(power_usage_df):
            power_usage_df = grouped
            power_usage_df = power_usage_df.fillna(method='ffill')
        # convert kw to kwh
        power_usage_df['value'] *= (15/60.0)
        logger.debug('After convert and split: {}'.format(power_usage_df))
        return power_usage_df, ''

    @staticmethod
    def validate_query(ship_id, start, end):
        if not ship_id:
            return 'spaceship_id not found'
        elif not start:
            return 'start time not found'
        elif not end:
            return 'end time not found'
        try:
            pd.Timestamp(start)
        except ValueError:
            return 'invalid start time: ' + start
        try:
            pd.Timestamp(end)
        except ValueError:
            return 'invalid end time: ' + end
        return ''

    @staticmethod
    def format_iso_str(date='2018-08-24T00:20:00Z'):
        t = dateparser.parse(date)
        formatted_t = t.strftime("%A, %d %B, %Y at %X")
        return formatted_t


    @staticmethod
    def db_obj_to_query_response(from_db, log):
        '''
            TODO convert db object to expected format
        '''
        log.debug('Got obj: {}'.format(from_db))
        return json.dumps({'id': 77}), ''



