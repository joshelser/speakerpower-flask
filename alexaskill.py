#!flask/bin/python

from flask import Flask, render_template, request
from flask_ask import Ask, statement
import json, logging, os, urllib2

app = Flask(__name__)
ask = Ask(app, '/')

baseurl = 'https://secure.penguinsinabox.com/speakerpower'
username = 'alexa'
password = os.environ['password']

@ask.intent('TurnOnIntent')
def off():
    data = request.data
    parsed_data = json.loads(data)
    request('/on')
    return statement('Ok')

@ask.intent('TurnOffIntent')
def off():
    data = request.data
    parsed_data = json.loads(data)
    request('/off')
    return statement('Ok')

def request(suffix):
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    baseurl = os.environ['baseurl']
    password_mgr.add_password(None, baseurl, username, password)
    handler = urllib2.HTTPBasicAuthHandler(password_mgr)
    opener = urllib2.build_opener(handler)
    urllib2.install_opener(opener)
    try:
        response = urllib2.urlopen(baseurl + suffix)
    except urllib2.HTTPError as e:
        print "Error: %d" % (e.code)

if __name__ == '__main__':
    app.run(debug=True)
