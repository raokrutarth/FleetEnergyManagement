
from flask import Flask
from datetime import datetime
import re
import dateutil.parser as dateparser

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Flask Home </h1>"

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

    content = "Hello there, " + clean_name + "! It's " + formatted_now
    return content

@app.route("/hello")
def hello2():
    now = datetime.now().utcnow()
    t = dateparser.parse('2018-08-24T00:20:00Z')
    res = str(now) + '</br>' + str(t)
    return res