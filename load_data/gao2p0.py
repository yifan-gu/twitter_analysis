#!/usr/bin/env python

import sys,os
import subprocess
import json
import datetime
import calendar
import struct


def load(js_output, tid, uid, ts, tx, rt):

    if len(rt) > 0:
        js_output.write(
            json.dumps({'tid':tid, 'uid':uid, 'ts':ts, 'tx':tx, 'rt':rt}) + '\n'
            )
    else:
        js_output.write(
            json.dumps({'tid':tid, 'uid':uid, 'ts':ts, 'tx':tx}) + '\n'
            )

def cao(js_output, tweet_json):
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
    #text = tweet['text'].encode('utf8').replace('\n', '\\n').replace('"', '\\"').replace('\\', '\\\\')
    #text = "\\n".join(sp)
    #output.write( u"{}\t{}\t{}\t{}\t{}\n".format(
                        #tweet['id_str'],
                        #tweet['user']['id_str'],
                        #tweet['retweeted_status']['user']['id_str'] if tweet.has_key('retweeted_status') else "",
                        #ts,
                        #text.decode('utf8')
                    #).encode('utf8')
                #)
    load( js_output,
          int(tweet['id_str'] ),
          int(tweet['user']['id_str'] ),
          int(ts ),
          tweet['text'],
          tweet['retweeted_status']['user']['id_str'] if tweet.has_key('retweeted_status') else "",
          )


def gao(s3_path, suffix):

    filename = s3_path.split('/')[-1]
    subprocess.check_call(
        "s3cmd get {0}".format(s3_path),
        shell=True
        )
    js_output = open(filename+suffix, 'w')
    with open(filename, "r") as f:
        for line in f:
            if line.rstrip() != "":
                cao(js_output, line.rstrip() )

    f.close()
    js_output.close()
    os.remove(filename )

js_list = open('jsonlist.txt', 'w')
with open("./raw_list.txt", "r") as f:
    for line in f:
        if line.rstrip() != "":
            s3path = line.rstrip().split()[-1]
            suffix = '_processed'
            gao(s3path, suffix)
            js_list.write(s3path.split('/')[-1]+suffix+'\n')

f.close()
js_list.close()
