import datetime
import calendar
from flask import Flask
from flask import request
from backend import getdata
import traceback
from time import gmtime, strftime

app = Flask(__name__)
g = getdata.getdata('backend/table_config.txt')
team_str = 'supercloud,5830-2688-4282\n'

@app.route('/')
def hello_world():
    return 'Ehh! Please choose between q1, q2, q3, q4.'


@app.route('/q1')
def q1():
    return team_str + strftime('%Y-%m-%d %H:%M:%S', gmtime()) + '\n'


@app.route('/q2')
def q2():
    ts = calendar.timegm( datetime.datetime.strptime(
        request.args.get('time', ''),
        "%Y-%m-%d %H:%M:%S").utctimetuple()
    )
    result = g.query2(ts)
    if len(result) <= 0:
	return team_str + 'Nothing found'

    #print result
    buf = '\n'.join(result)
    return team_str + buf + '\n'


@app.route('/q3')
def q3():
    start = request.args.get('userid_min', '')
    end = request.args.get('userid_max', '')
    return team_str + str(g.query3(int(start), int(end))) + '\n'
    #return g.query3(int("{}, {}".format(
    #    request.args.get('userid_min', ''),
    #    request.args.get('userid_max', '')
    #)


@app.route('/q4')
def q4():
    result = sorted(g.query4(int(request.args.get('userid', ''))))
    if len(result) <= 0:
	return team_str + 'Nothing found'
    buf = ''
    #print result
    for i in result:
	buf += str(i) + '\n'
    #print buf
    return team_str + buf
	

if __name__ == '__main__':
    app.run()
