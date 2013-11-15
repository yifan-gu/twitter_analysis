var express = require('express');
var app = express();

app.get('/q1', function (req, res) {
  res.send('supercloud q1!');
});

app.get('/q2', function (req, res) {
  var create_time = req.param('time');
  res.send('supercloud q2 = time: ' + create_time + '!');
});

app.get('/q3', function (req, res) {
  var uid_min = req.param('userid_min');
  var uid_max = req.param('userid_max');
  res.send('supercloud q3 = userid_min: ' + uid_min + ', userid_max: ' + uid_max + '!');
});

app.get('/q4', function (req, res) {
  var userid = req.param('userid');
  res.send('supercloud q4 = userid: '+ userid + '!');
});

app.listen(3000);
console.log('Listening on port 3000');
