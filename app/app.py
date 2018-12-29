


from flask import Flask, request, Response
from datetime import datetime
import dateutil.parser as dateparser
from http import HTTPStatus

from debug import get_logger
from energy import parse_data, respond

app = Flask(__name__)
logger = get_logger()

@app.route("/")
def home():
    logger.warning('Root path called. Serving error message.')
    return "<h1>Invalid URL</h1>", HTTPStatus.BAD_REQUEST

@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        return parse_data(
            request.get_json(),
            logger
        )
    if request.method == 'GET':
        # id = request.args['spaceship_id'] #if key doesn't exist, returns a 400, bad request error
        return respond(
            request.args.get('spaceship_id'),
            request.args.get('start'),
            request.args.get('end'),
            logger
        )

@app.route("/test/<id>")
def id_test(id):
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")
    content = "Got id " + id + ". Time: " + formatted_now
    logger.warning('[+] Some warning message')
    return content

@app.route("/date")
def date():
    now = datetime.now().utcnow()
    t = dateparser.parse('2018-08-24T00:20:00Z')
    res = str(now) + '</br>' + str(t)
    logger.info("[+] Useful Info message")
    return res