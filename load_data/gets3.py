#!/usr/bin/python

import subprocess

d = open('./jsonlist.txt', 'w')
with open("./rawlist.txt", "r") as f:
    for s3_path in f:
        subprocess.check_call(
        "s3cmd get {0}".format(s3_path.split()[-1]),
        shell=True
        )
        filename = s3_path.split()[-1].split('/')[-1]
        d.write(filename + '\n')
f.close()
d.close()
