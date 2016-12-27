#!flask/bin/python
from flask import Flask, render_template
import RPi.GPIO as gpio
import logging, os

app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

power = 16
state_file = '/tmp/speakerpower.state'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/state')
def state():
    return 'On' if gpio.input(power) else 'Off'

@app.route('/on')
def on():
    gpio.output(power, gpio.HIGH)
    set_state(gpio.HIGH)
    return 'OK -- on'

@app.route('/off')
def off():
    gpio.output(power, gpio.LOW)
    set_state(gpio.LOW)
    return 'OK -- off'

@app.route('/status')
def status():
    return 'OK'
    
@app.before_first_request
def setup():
    gpio.setwarnings(False)
    gpio.setmode(gpio.BOARD)
    gpio.setup(power, gpio.OUT)
    # Start with it off to avoid it being HIGH on automatic-start
    gpio.output(power, get_state())

def set_state(state):
    with open(state_file, 'w') as f:
        if gpio.LOW == state:
            f.write(0)
        else:
            f.write(1)

def get_state():
    if not os.path.isfile(state_file):
        return gpio.LOW
    with open(state_file, 'r') as f:
        byte = f.read(1)
        if 1 == byte:
            return gpio.HIGH
        return gpio.LOW

if __name__ == '__main__':
    setup(get_state())
    app.run(debug=True)
