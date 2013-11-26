var http = require('http');

http.createServer(function (req, res) {
  //var body = "hello, world";
  //res.writeHead(200, {'Content-Type': 'text/plain', 'Content-Length': body.length});
  //res.write("hello, world");
  qqq = req.url.substring(0, 3);

  if(qqq == "/q1"){
    res.writeHead(200, {'Content-Type': 'text/plain'});
    res.write("q1");
  }
  else if(qqq == "/q2"){
    var create_time = req.url.substring(9);
    var pattern = /(\d{4})-(\d{2})-(\d{2})\+(\d{2}):(\d{2}):(\d{2})/;
    var myArray = pattern.exec(create_time);
    var timestamp = Date.UTC(
                      parseInt(myArray[1]),
                      parseInt(myArray[2]) - 1,
                      parseInt(myArray[3]),
                      parseInt(myArray[4]),
                      parseInt(myArray[5]),
                      parseInt(myArray[6])
                   ) / 1000;

    res.writeHead(200, {'Content-Type': 'text/plain'});
    res.write("q2, time: " + timestamp);
  }
  else if(qqq == "/q3"){

    var i = req.url.indexOf('max');
    var uid_min = req.url.substring(15, i - 8);
    var uid_max = req.url.substring(i+4);
    res.writeHead(200, {'Content-Type': 'text/plain'});
    res.write("q3, userid_min: " + uid_min + ", userid_max: " + uid_max);
  }
  else if(qqq == "/q4"){
    var uid= req.url.substring(11);
    res.writeHead(200, {'Content-Type': 'text/plain'});
    res.write("q4, userid: " + uid);
  }

  res.end();
}).listen(3000);

console.log("start listening on port 3000");
