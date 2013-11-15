console.log(
  (new Date("Wed Aug 27 13:08:45 +0000 2008")).getTime()
);

var re = /(\d{4})-(\d{2})-(\d{2})\+(\d{2}):(\d{2}):(\d{2})/;
array = re.exec("2013-08-27+13:08:45");
console.log(
  (new Date(array[1],
            array[2],
            array[3],
            array[4],
            array[5],
            array[6]
    )).getTime()
);
