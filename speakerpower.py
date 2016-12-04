#!flask/bin/python
from flask import Flask, render_template
import RPi.GPIO as gpio

app = Flask(__name__)
power = 16

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/state')
def state():
    return 'On' if gpio.input(power) else 'Off'

@app.route('/on')
def on():
    gpio.output(power, gpio.HIGH)
    return 'OK -- on'

@app.route('/off')
def off():
    gpio.output(power, gpio.LOW)
    return 'OK -- off'
    
@app.before_first_request
def setup():
    gpio.setwarnings(False)
    gpio.setmode(gpio.BOARD)
    gpio.setup(power, gpio.OUT)
    # Start with it off to avoid it being HIGH on automatic-start
    gpio.output(power, gpio.LOW)

if __name__ == '__main__':
    setup()
    app.run(debug=True)
