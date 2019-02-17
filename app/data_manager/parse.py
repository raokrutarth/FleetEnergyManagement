# Author: Krutarth Rao
# Email: raok@purdue.edu

from datetime import datetime
import dateutil.parser as dateparser
import pandas as pd
import numpy as np
import json


# db & parsing constants
TIME_FREQ = '15T' # 15 mins
DB_TIMESERIES = 'energy'
POWER_ENERGY_RATIO_15M = (15/60.0)

# input data keys
SHIPID_KEY = 'spaceship_id'
UNITS_KEY = 'units'
DATA_KEY = 'data'
POWER_UNIT = 'kW'
ENERGY_UNIT = 'kWh'
TS_KEY = 'datetime'
VALUE_KEY = 'value'


class Parser:

    @staticmethod
    def make_timeseries_df(data, log):
        try:
            df = pd.DataFrame(data)
            if len(df) == 0:
                return None, 'empty data object'
            if not set([TS_KEY, VALUE_KEY]).issubset(df.columns):
                # verify each time event has the required labels
                log.debug('invalid labels in data object. \nexpected: {}\ngot: {}'\
                    .format(set([TS_KEY, VALUE_KEY]), df.columns))
                return None, 'invalid labels in data object'
            if any(df[VALUE_KEY] < 0):
                return None, 'got negative values in data. Negative power/energy usage not allowed'
            df[TS_KEY] = pd.to_datetime(df[TS_KEY], utc=True)
            df[VALUE_KEY] = df[VALUE_KEY].astype('float')

            if df[TS_KEY].isnull().any().any():
                log.error('missing timestamp for a datapoint in {}'.format(data))
            if df[VALUE_KEY].isnull().any().any():
                log.error('missing value for a datapoint in {}'.format(data))

            df.dropna(inplace=True)
            df = df.set_index(TS_KEY)
            df = df.sort_index()

            if not pd.Series(df.index).is_unique:
                return None, 'duplicate timestamps detected in energy/power usage data'
            log.info('Timeseries dataframe created for {}'.format(data))
            return df, ''
        except ValueError:
            log.debug('Invalid values in "data" object detected: {}'.format(data))
            return None, 'invalid values in data object'
        except KeyError:
            log.debug('Invalid/missing labels in data object detected: {}'.format(data))
            return None, 'invalid labels in data object'
        except Exception as e:
            log.error('Unknown error parsing data object: {}'.format(data))
            log.error(e)
            return None, 'unknown error parsing data object'


    @staticmethod
    def validate_parse_consumption_data(consumption_info, log):
        if not consumption_info:
            return None, 'missing json object in request'

        for label in set([SHIPID_KEY, UNITS_KEY, DATA_KEY]):
            if label not in consumption_info:
                return None, "missing {} in input fields".format(label)

        if consumption_info[UNITS_KEY].lower() not in set([POWER_UNIT.lower(), ENERGY_UNIT.lower()]):
            return None, 'invalid units {}'.format(consumption_info[UNITS_KEY])

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
        power_usage_df['value'] *= POWER_ENERGY_RATIO_15M
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
        return Parser.validate_start_and_end(start, end)

    @staticmethod
    def validate_start_and_end(start, end):
        err = ''
        try:
            pd.Timestamp(start)
        except ValueError:
            err += 'invalid start time: %s ' % start
        try:
            pd.Timestamp(end)
        except ValueError:
            err += 'invalid end time: %s' % end
        if start > end:
            err += 'start time greater that end time'
        return err

    @staticmethod
    def db_obj_to_query_response(ship_id, from_db, log):
        '''
            converts and constructs the response from
            the data fetched from the database
        '''
        try:
            ship_id = int(ship_id)
        except ValueError:
            log.warning('Got non-int ship id: %s' % ship_id)

        log.debug('Got db object to convert: {}'.format(from_db))
        try:
            df = from_db[DB_TIMESERIES].astype('float')
        except (ValueError, KeyError):
            log.error('Unable to convert db returned object to dataframe')
            return '', 'unable to parse data during fetch'

        resp = {
            SHIPID_KEY: ship_id,
            UNITS_KEY:ENERGY_UNIT,
            DATA_KEY: list(),
        }
        for timestamp, row in df.iterrows():
            resp[DATA_KEY].append({
                TS_KEY: timestamp.isoformat().replace('+00:00', 'Z'),
                VALUE_KEY: int(row[VALUE_KEY])
            })
        log.debug('resp before json dumps: {}'.format(resp))
        json_str = json.dumps(resp)
        return json_str, ''



# Author: Krutarth Rao
# Email: raok@purdue.edu