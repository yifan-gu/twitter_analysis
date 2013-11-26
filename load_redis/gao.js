var fs = require('fs');

function gao(filename) {
  var data = fs.readFileSync(filename, 'utf8');
  var content = data.split('\n').filter(function (line) {
    return line;
  });
  for (var i=0; i < content.length; ++i) {
    var tweet = JSON.parse(content[i]);
    var ts = Date.parse(tweet['created_at']) / 1000;
    console.log(ts);
  }
}

gao('small.json');
