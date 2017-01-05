#!flask/bin/python

from flask import Flask, render_template, request
from flask_ask import Ask, statement
import os, random, urllib2

app = Flask(__name__)
app.config['ASK_APPLICATION_ID'] = 'amzn1.ask.skill.0fb55066-1cb6-410c-92ef-5e78bf60b0fe'
ask = Ask(app, '/')

baseurl = 'https://secure.penguinsinabox.com/speakerpower'
username = 'alexa'
password = os.environ['password']
responses = ['ok', 'alright', 'sure', 'done']

@ask.intent('TurnOnIntent')
def off():
    request('/on')
    return statement(random.choice(responses))

@ask.intent('TurnOffIntent')
def off():
    request('/off')
    return statement(random.choice(responses))

def request(suffix):
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
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
