
from http import HTTPStatus


try:
    from .file_ops import FileOps
    from .parse import Parser
except ImportError:
    from file_ops import FileOps
    from parse import Parser


def ingest_data_and_respond(data, logger):
    logger.info('Got POSTed data: {}'.format(data))
    valid, err = Parser.validate_consumption_data(data, logger)
    if not valid:
        return err, HTTPStatus.BAD_REQUEST

    new_entry = {
        'id': data['spaceship_id']
    }

    data['units'] = data['units'].lower()
    if data['units'] == 'kwh':
        new_entry['TS'], err = Parser.split(data['data'], logger)
    elif data['units'] == 'kw':
        new_entry['TS'], err = Parser.convert_and_split(data['data'], logger)

    if err != '':
        return err, HTTPStatus.BAD_REQUEST
    logger.debug('Saving entry: {}'.format(new_entry))
    FileOps.save_entry(new_entry)
    return 'Successfully POSTed'

def respond(ship_id, start, end, logger):
    logger.info('Got params: ship_id: {}, start: {}, end: {}'.format(ship_id, start, end))
    saved = FileOps.read()
    logger.debug("Retrived saved data: {}".format(saved))
    return saved