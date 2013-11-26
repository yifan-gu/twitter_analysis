var http = require('http');
var cluster = require('cluster');
var async = require('async');
var mysql = require('mysql');
var NodeCache = require('node-cache');
var cache = new NodeCache( { stdTTL: 1, checkperiod: 0 } );
require("date-format-lite")
Date.masks.default = 'YYYY-MM-DD+hh:mm:ss'
var teamstr = "supercloud, 5830-2688-4282\n";

//var express = require('express');
//var app = express();
var map = {};
//var arypos = [];
//var arycnt = [];
var conn;

async.series({
  loadtb4: function(callback) {
    conn = mysql.createConnection({
      host : 'localhost',
      user : 'root',
      database : 'cloud',
    });
    
    conn.connect(function(err) {
      if (err) {
        console.log(err);
      }
      //callback(null, 1);

    });
    
    conn.query('select * from tb4', function(err, rows) {
      var i = 0;
      rows.forEach(function(row) {
        map[row['id']] = row['users'];
        
        if (++i % 100000 == 0) {
          console.log('line ' + i);
        }
      });
    
      console.log('tb4 load done');
      callback(null, 1);
    });
  },

  create_server: function(callback) {
    /*if (cluster.isMaster) {
      for (var i = 0; i < 0; i++) {
      cluster.fork();
      }
      } else {*/
    http.createServer(function (req, res) {
      //var body = "hello, world";
      //res.writeHead(200, {'Content-Type': 'text/plain', 'Content-Length': body.length});
      //res.write("hello, world");
      qqq = req.url.substring(0, 3);

      if(qqq == "/q1"){
        cache.get("time", function(err, kv) {
          //console.log(kv);
          var datestr;
          if (Object.keys(kv).length == 0) {
            var now = new Date();
            datestr = now.format();
            cache.set("time", datestr);
          } else {
            datestr = kv["time"]
          }
          
          res.writeHead(200, {'Content-Type': 'text/plain'});
          res.end(teamstr + datestr + '\n');
        });
        
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
        var uid_min = req.url.substring(14, i - 8);
        var uid_max = req.url.substring(i+4);
        conn.query('select count from tb3 where id < ' + uid_min + ' order by id desc limit 1', function(err, rows){
          if (!rows) {
            min_cnt = 0;
          }

          min_cnt = rows[0]['count'];
          conn.query('select count from tb3 where id <= ' + uid_max + ' order by id desc limit 1', function(err, rows){
            // TODO out of bound
            var max_cnt = rows[0]['count'];
            res.writeHead(200, {'Content-Type': 'text/plain'});
            res.end(teamstr + (max_cnt - min_cnt) + '\n');
          });
        });
      }
      else if(qqq == "/q4"){
        var uid= req.url.substring(11);
        res.writeHead(200, {'Content-Type': 'text/plain'});
        data = map[uid];
        //console.log(data);
        if (data) {
          res.end(teamstr + data);
        } else {
          res.end(teamstr);
        }
      }
      
    }).listen(80);

    console.log("start listening on port 80");
    //}
    callback(null, 2);
  },
});