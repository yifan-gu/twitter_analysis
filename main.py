import datetime
import calendar
from flask import Flask
from flask import request
from backends import getdata

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'SB! Please choose between q1, q2, q3, q4.'


@app.route('/q1')
def q1():
    return 'q1'


@app.route('/q2')
def q2():
    ts = calendar.timegm( datetime.datetime.strptime(
        request.args.get('time', ''),
        "%Y-%m-%d %H:%M:%S").utctimetuple()
    )
    return str(ts)


@app.route('/q3')
def q3():
    return "{}, {}".format(
        request.args.get('userid_min', ''),
        request.args.get('userid_max', '')
    )


@app.route('/q4')
def q4():
    return request.args.get('userid', '')

if __name__ == '__main__':
    app.run()
