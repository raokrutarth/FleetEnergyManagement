
from http import HTTPStatus
from flask import Response
from json import dumps
try:
    from .parse import Parser
    from .db_ops import DBManager
except ImportError:
    from parse import Parser
    from db_ops import DBManager


def ingest_data_and_respond(data, log):
    log.info('Got POSTed data: {}'.format(data))
    timeseries_df, err = Parser.validate_parse_consumption_data(data, log)
    if err != '':
        return err, HTTPStatus.BAD_REQUEST

    ship_id = data['spaceship_id']
    units = data['units'].lower()

    if units == 'kwh':
        timeseries, err = Parser.split(timeseries_df, log)
    elif units == 'kw':
        timeseries, err = Parser.convert_and_split(timeseries_df, log)

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
        return {'error': err}, HTTPStatus.BAD_REQUEST

    try:
        ship_id = int(ship_id)
    except ValueError:
        ship_id = str(ship_id)

    log.info('Got params: ship_id: {}, start: {}, end: {}'.format(ship_id, start, end))
    db_obj = DBManager.get_energy_entry(ship_id, start, end, log)
    log.debug("Retrived saved data: {}".format(db_obj))
    resp, err = Parser.db_obj_to_query_response(db_obj, log)
    if err != '':
        return err, HTTPStatus.SERVICE_UNAVAILABLE
    log.debug('Converted retrived to json response: {}'.format(resp))
    return Response(resp, status=HTTPStatus.OK, mimetype='application/json')
