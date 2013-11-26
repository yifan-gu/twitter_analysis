#!/usr/bin/env node

var redis = require("redis");

client = redis.createClient();

client.on("error", function (err) {
    console.log("error event - " + client.host + ":" + client.port + " - " + err);
});


client.keys("*", function (err, keys) {
  var counter = 0;
  var total = keys.length;
  keys.forEach(function (key, pos) {
    client.lrange(key, 0, -1, function (err, data) {
      if(err){
        console.log(err);
        return;
      }
      arr = []
      for (var i=0; i < data.length; ++i) {
        arr.push(data[i].split(':', 2))
      }
      arr.sort(function (a, b) {
        return a[0] - b[0];
      });

      for (var i=0; i < arr.length; ++i) {
        arr[i] = arr[i][0] + ':' + arr[i][1]
      }

      value = arr.join('\n');

      client.del(key, function (err) {
        if(err){
          console.log(err);
          return;
        }
        client.set(key, value, function (err) {
          if(err){
            console.log(err);
            return;
          }
          counter = counter + 1;
          if(counter == total){
            console.log("finished");
            client.quit(function (err, res) {
                console.log("Exiting from quit command.");
            });
          }
        });
      })

    });

  });

});

