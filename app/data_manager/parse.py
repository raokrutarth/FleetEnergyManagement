

from datetime import datetime
import dateutil.parser as dateparser
import pandas as pd
import numpy as np



class Parser:
    @staticmethod
    def validate_consumption_data(consumption_info, log):
        keys = ["spaceship_id", "units", "data"]
        for k in keys:
            if k not in consumption_info:
                return False, "missing {} in input fields".format(k)
        if consumption_info['units'].lower() != 'kwh' and consumption_info['units'].lower() != 'kw':
            return False, 'invalid units {}'.format(consumption_info['units'])

        try:
            if len(pd.DataFrame(consumption_info['data']).columns) != 2:
                log.debug('Got invalid labels in data object: {}'.format(consumption_info['data']))
                return False, 'invalid labels in "data"'
        except:
            log.debug('Got invalid data object: {}'.format(consumption_info['data']))
            return False, 'invaild object in "data"'
        return True, ''

    @staticmethod
    def split(energy_usage_log, logger):
        '''
            splits an energy timeseries to a 15-min interval
            timeseries
        '''
        df = pd.DataFrame(energy_usage_log)
        try:
            df['datetime'] = pd.to_datetime(df['datetime'], utc=True)
            df = df.set_index('datetime')
            df = df.sort_index()
            df = df.resample('15T').sum()
        except ValueError:
            return None, 'invalid time stamps passed in "data"'
        logger.debug('After split: {}'.format(df))
        return df.to_json(orient='records'), ''

    @staticmethod
    def convert_and_split(power_usage_log, logger):
        '''
            Converts kW data to kWh
        '''
        df = pd.DataFrame(power_usage_log)
        df['datetime'] = pd.to_datetime(df['datetime'])
        df = df.set_index('datetime')
        df = df.sort_index()
        print('Pre: \n', df)
        df = pd.DataFrame(power_usage_log)
        try:
            df['datetime'] = pd.to_datetime(df['datetime'], utc=True)
            df = df.set_index('datetime')
            df = df.sort_index()
            df = df.resample('15T').mean()
            df = df.fillna(method='ffill')
            df['value'] *= (15/60.0)
        except ValueError:
            return None, 'invalid time stamps passed in "data"'
        except KeyError:
            return None,
        logger.debug('After convert and split: {}'.format(df))
        return df.to_json(orient='records'), ''

    @staticmethod
    def funcname(parameter_list):
        t = dateparser.parse('2018-08-24T00:20:00Z')
        formatted_t = t.strftime("%A, %d %B, %Y at %X")
        return

