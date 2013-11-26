#!/usr/bin/env python

import subprocess

def s3_get(s3_path):
    filename = s3_path.split('/')[-1]
    subprocess.check_call(
            "s3cmd get {} && mv {} small.json".format(s3_path, filename),
            shell=True
        )
    subprocess.check_call(
            "./merge.sh"
        )

with open('jsonlist.txt', 'r') as f:
    for line in f:
        if line.strip() != "":
            s3_get(line.strip())

