
from http import HTTPStatus


def save(lines):
    f = open('data.txt', 'a+')
    for line in lines:
        f.write(line)
    f.close()

def read():
    try:
        with open('data.txt', 'r') as f:
            return f.read()
    except FileNotFoundError:
        return ''

def parse_data(data, logger):
    logger.info('Got POSTed data: {}'.format(data))
    save([repr(data)])
    return 'Successfully POSTed'

def respond(ship_id, start, end, logger):
    logger.info('Got params: ship_id: {}, start: {}, end: {}'.format(ship_id, start, end))
    saved = read()
    logger.debug("Got saved data: {}".format(saved))
    return saved