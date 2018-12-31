

from datetime import datetime
import dateutil.parser as dateparser
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
                return False, "missing {} in input fields".format(k)
        if consumption_info['units'].lower() not in UNITS:
            return False, 'invalid units {}'.format(consumption_info['units'])
        # verify each time event only has 2 labels
        try:
            df = pd.DataFrame(consumption_info['data'])
            if not COLUMNS.issuperset(df.columns):
                log.debug('Got invalid labels in data object. \nexpected: {}\ngot: {}'.format(
                    COLUMNS,
                    df.columns
                    )
                )
                return False, 'invalid labels in "data"'
        except Exception as e:
            log.debug('Got invalid data object: {}'.format(consumption_info['data']), e)
            return False, 'invaild object in "data"'
        return True, ''

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
        # df = df.resample(TIME_FREQ, label='right').sum()
        df = df.groupby(pd.Grouper(freq=TIME_FREQ, label='right')).sum()
        logger.debug('After split: {}'.format(df))
        return df.to_json(orient='records', index=True), ''


    @staticmethod
    def convert_and_split(power_usage_log, logger):
        '''
            Converts kW data to kWh

            TODO verify conversion
        '''
        df, err = Parser.make_timeseries_df(power_usage_log, logger)
        if err != '':
            return None, err
        df = df.groupby(pd.Grouper(freq=TIME_FREQ, label='right')).mean()
        df = df.fillna(method='ffill')
        # convert kw to kwh
        df['value'] *= (15/60.0)
        logger.debug('After convert and split: {}'.format(df))
        return df.to_json(orient='records', index=True), ''

    @staticmethod
    def funcname(parameter_list):
        t = dateparser.parse('2018-08-24T00:20:00Z')
        formatted_t = t.strftime("%A, %d %B, %Y at %X")
        return

