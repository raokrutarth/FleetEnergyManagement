
from http import HTTPStatus
try:
    from .parse import Parser
    from .db_ops import DBManager
except ImportError:
    from parse import Parser
    from db_ops import DBManager


def ingest_data_and_respond(data, log):
    log.info('Got POSTed data: {}'.format(data))
    err = Parser.validate_consumption_data(data, log)
    if err != '':
        return err, HTTPStatus.BAD_REQUEST

    ship_id = data['spaceship_id']
    units = data['units'].lower()
    ts_data = data['data']

    if units == 'kwh':
        timeseries, err = Parser.split(ts_data, log)
    elif units == 'kw':
        timeseries, err = Parser.convert_and_split(ts_data, log)

    if err != '':
        return err, HTTPStatus.BAD_REQUEST

    log.debug('Saving dataframe: {} \nfor ship_id: : {}'.format(
        timeseries,
        ship_id,
        )
    )

    if not DBManager.save_energy_entry(ship_id, timeseries):
        log.error('db save failed for ship: {}'.format(ship_id))
        log.error('timeseries: {}'.format(timeseries))
        res = DBManager.get_full_energy_entry(ship_id)
        log.error('full ship info in db befre fail: {}'.format(res))
        return 'DB error', HTTPStatus.SERVICE_UNAVAILABLE

    return 'Data saved successfully for ship {}'.format(ship_id)



def respond_to_query(ship_id, start, end, log):
    err = Parser.validate_query(ship_id, start, end)
    if err != '':
        return err, HTTPStatus.BAD_REQUEST

    log.info('Got params: ship_id: {}, start: {}, end: {}'.format(ship_id, start, end))
    res = DBManager.get_energy_entry(ship_id, start, end)
    log.debug("Retrived saved data: {}".format(res))
    return res