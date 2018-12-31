
from http import HTTPStatus
import json
import pandas as pd
try:
    from .file_ops import FileOps
    from .parse import Parser
    from .db_ops import DBManager
except ImportError:
    from file_ops import FileOps
    from parse import Parser
    from db_ops import DBManager


def ingest_data_and_respond(data, logger):
    logger.info('Got POSTed data: {}'.format(data))
    valid, err = Parser.validate_consumption_data(data, logger)
    if not valid:
        return err, HTTPStatus.BAD_REQUEST

    ship_id = data['spaceship_id']

    data['units'] = data['units'].lower()
    if data['units'] == 'kwh':
        timeseries, err = Parser.split(data['data'], logger)
    elif data['units'] == 'kw':
        timeseries, err = Parser.convert_and_split(data['data'], logger)

    if err != '':
        return err, HTTPStatus.BAD_REQUEST
    logger.debug('Saving dataframe: {} \nfor ship_id: : {}'.format(
        timeseries,
        ship_id,
        )
    )
    db_res = DBManager.save_entry(data['spaceship_id'], timeseries)
    if not db_res:
        logger.info('db save failed for: {}'.format(timeseries))
        res = DBManager.get_full_entry(data['spaceship_id'])
        logger.debug('full ship info in db befre fail: {}'.format(res))
        return 'DB error', HTTPStatus.INSUFFICIENT_STORAGE



def respond(ship_id, start, end, logger):
    if not ship_id:
        return 'spaceship_id not found'
    elif not start:
        return 'start time not found'
    elif not end:
        return 'end time not found'
    # validate datetime
    logger.info('Got params: ship_id: {}, start: {}, end: {}'.format(ship_id, start, end))
    res = DBManager.get_entry(ship_id, start, end)
    logger.debug("Retrived saved data: {}".format(res))
    return res