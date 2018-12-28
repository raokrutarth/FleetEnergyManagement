
from flask import Flask
from datetime import datetime
import re
import dateutil.parser as dateparser
import logging

app = Flask(__name__)
logger = logging.getLogger()
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(message)s'
)
# create a file handler
log_to_file = logging.FileHandler('power_service.log')
log_to_file.setLevel(logging.DEBUG)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_to_file.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(log_to_file)

@app.route("/")
def home():
    logger.debug('[-] My debug message')
    return "<h1>Flask Home 2</h1>"

@app.route("/hello/<name>")
def hello_there(name):
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")

    # Filter the name argument to letters only using regular expressions. URL arguments
    # can contain arbitrary text, so we restrict to safe characters only.
    match_object = re.match("[a-zA-Z]+", name)

    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = "Friend"

    content = "Hello you, " + clean_name + "! It's " + formatted_now
    logger.warning('[+] Some warning message')
    return content

@app.route("/hello")
def hello2():
    now = datetime.now().utcnow()
    t = dateparser.parse('2018-08-24T00:20:00Z')
    res = str(now) + '</br>' + str(t)
    print('[+] before logger')
    logger.info("[+] Useful Info message")
    return res