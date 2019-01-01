

from datetime import datetime
import dateutil.parser
import pandas as pd
import numpy as np


TIME_FREQ = '15T' # 15 mins
OUTER_KEYS = set(["spaceship_id", "units", "data"])
UNITS = set(['kw', 'kwh'])
COLUMNS = set(['datetime', 'value'])


class Parser:

    @staticmethod
    def validate_consumption_data(consumption_info, log):
        for k in OUTER_KEYS:
            if k not in consumption_info:
                return "missing {} in input fields".format(k)
        if consumption_info['units'].lower() not in UNITS:
            return 'invalid units {}'.format(consumption_info['units'])
        # verify each time event only has 2 labels
        try:
            df = pd.DataFrame(consumption_info['data'])
            if not COLUMNS.issuperset(df.columns):
                log.debug('Got invalid labels in data object. \nexpected: {}\ngot: {}'.format(
                    COLUMNS,
                    df.columns
                    )
                )
                return 'invalid labels in "data"'
        except Exception as e:
            log.debug('Unknown exception due to data object: {}'.format(consumption_info['data']), e)
            return 'invaild object in "data"'
        return ''

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
    def make_timeseries_df(data, log):
        try:
            df = pd.DataFrame(data)
            df['datetime'] = pd.to_datetime(df['datetime'], utc=True)
            df = df.set_index('datetime')
            df = df.sort_index()
            log.info('Timeseries dataframe created for {}'.format(data))
            return df, ''
        except ValueError:
            log.debug('Invalid values in "data" object detected: {}'.format(data))
            return None, 'invalid data object'
        except KeyError:
            log.debug('Invalid/missing keys in data object detected: {}'.format(data))
            return None, 'invalid data object'
        except Exception as e:
            log.error('Unknown error parsing data object: {}'.format(data))
            log.error(e)
            return None, 'unknown error parsing data object'

    @staticmethod
    def split(energy_usage_log, logger):
        '''
            splits an energy timeseries to a 15-min interval
            timeseries

            TODO verify disaggregation & aggregation timestamps
        '''
        df, err = Parser.make_timeseries_df(energy_usage_log, logger)
        if err != '':
            return None, err
        grouped = df.groupby(pd.Grouper(freq=TIME_FREQ, label='right')).sum()
        # keep original data if already 15-min spaced
        if len(grouped) != len(df):
            df = grouped
        logger.debug('After split: {}'.format(df))
        return df, ''

    @staticmethod
    def convert_and_split(power_usage_log, logger):
        '''
            Converts kW data to kWh

            TODO verify conversion
        '''
        df, err = Parser.make_timeseries_df(power_usage_log, logger)
        if err != '':
            return None, err
        grouped = df.groupby(pd.Grouper(freq=TIME_FREQ, label='right')).mean()
        # Don't change the labels if already 15min spaced
        if len(grouped) != len(df):
            df = grouped
            df = df.fillna(method='ffill')
        # convert kw to kwh
        df['value'] *= (15/60.0)
        logger.debug('After convert and split: {}'.format(df))
        return df, ''

    @staticmethod
    def format_iso_str(date='2018-08-24T00:20:00Z'):
        t = dateparser.parse(date)
        formatted_t = t.strftime("%A, %d %B, %Y at %X")
        return formatted_t

