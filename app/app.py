


from flask import Flask, request, Response, send_file
from http import HTTPStatus
import os

try:
    from .debug import get_logger
    from .data_manager.energy import ingest_data_and_respond, respond
except ImportError:
    from debug import get_logger
    from data_manager.energy import ingest_data_and_respond, respond_to_query

app = Flask(__name__)
log = get_logger()

@app.route("/")
def home():
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
        return respond_to_query(
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
    log.warning('forecast endpoint called')
    return '<h1>Not Implemented</h1>', HTTPStatus.NOT_IMPLEMENTED

@app.route("/usagechart",  methods=['GET'])
def send_chart_jpg():
    log.warning('usagechart endpoint called')
    chart_res = send_file('big.jpg', mimetype='image/jpg')
    return '<h1>Not Implemented</h1>', HTTPStatus.NOT_IMPLEMENTED
