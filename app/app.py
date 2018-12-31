


from flask import Flask, request, Response, send_file
from http import HTTPStatus
import os

try:
    from .debug import get_logger
    from .data_manager.energy import ingest_data_and_respond, respond
    from .data_manager.db_ops import DBManager
except ImportError:
    from debug import get_logger
    from data_manager.energy import ingest_data_and_respond, respond
    from data_manager.db_ops import DBManager

app = Flask(__name__)
log = get_logger()

@app.route("/")
def home():
    log.info('{}'.format(os.environ))
    DBManager.setup(log)
    log.warning('Root path called by client. Serving error message.')
    return "<h1>Invalid URL</h1>", HTTPStatus.METHOD_NOT_ALLOWED

@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        return ingest_data_and_respond(
            request.get_json(),
            log
        )
    if request.method == 'GET':
        return respond(
            request.args.get('spaceship_id'),
            request.args.get('start'),
            request.args.get('end'),
            log
        )

@app.route("/topusers/<count>",  methods=['GET'])
def topusers(count):
    log.warning('[+] Got count ' + count)
    return '<h1>Not Implemented</h1>', HTTPStatus.NOT_IMPLEMENTED

@app.route("/forecast",  methods=['GET'])
def forecast():
    log.warning('[+] Some warning message')
    return '<h1>Not Implemented</h1>', HTTPStatus.NOT_IMPLEMENTED

@app.route("/chart",  methods=['GET'])
def send_jpg():
    return send_file('big.jpg', mimetype='image/jpg')
