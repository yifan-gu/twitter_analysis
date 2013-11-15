#!/usr/bin/env python

import sys,os
import subprocess
import json
import datetime
import calendar

def cao(tweet_json, output):
    tweet = json.loads(tweet_json)
    # tweet id
    # user id
    # retweet uid
    # timestamp
    ts = calendar.timegm( datetime.datetime.strptime(
            ' '.join(tweet['created_at'].split(' ')[:4] + tweet['created_at'].split(' ')[5:]) ,
        "%a %b %d %X %Y").utctimetuple()
        )
    # text
    output.write( u"{}\t{}\t{}\t{}\t{}\n".format(
                        tweet['id_str'].zfill(20),
                        tweet['user']['id_str'].zfill(20),
                        tweet['retweeted_status']['user']['id_str'].zfill(20) if tweet.has_key('retweeted_status') else "",
                        ts,
                        tweet['text']
                    ).encode('utf8')
                )


def gao(s3_path):

    filename = os.path.basename(s3_path)
    subprocess.check_call(
            "s3cmd get {0}".format(s3_path),
            shell=True
            )
    with open(filename+"_output", "w") as output:
        with open(filename, "r") as f:
            for line in f:
                if line.rstrip() != "":
                    cao( line.rstrip() , output)

    os.remove(filename )


with open("./json_files", "r") as f:
    for line in f:
        if line.rstrip() != "":
            gao(line.rstrip())

