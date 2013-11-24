#!/usr/bin/env python

import sys,os
import subprocess
import json
import datetime
import calendar
import struct

ts_output = open('hb_ts', "w")
ud_output = open('hb_uid', "w")
rt_output = open('hb_rt', "w")

def load(tid, uid, ts, tx, rt):

    def barr2str(arr):
        return "\\x" + "\\x".join("{:02x}".format(ord(i)) for i in arr)

    ts_output.write(
            # put timestamp, tweet_ts, tweet:tw_id, text
            'put "timestamp", "{}", "tweet:{}","{}"\n'.format(
                barr2str(struct.pack(">Q", ts)),
                barr2str(struct.pack(">Q", tid)),
                tx)
            )
    ud_output.write(
            # put user, uid, tweet:tw_id, ""
            'put "user", "{}", "tweet:{}",""\n'.format(
                barr2str(struct.pack(">Q", uid)),
                barr2str(struct.pack(">Q", tid)) )
            )

    if rt == "":
        return

    rt_uid = int(rt)

    rt_output.write(
            # put retweet, rt_uid, tweet:tw_id, uid
            'put "retweet", "{}", "tweet:{}","{}"\n'.format(
                barr2str(struct.pack(">Q", rt_uid)),
                barr2str(struct.pack(">Q", tid)),
                barr2str(struct.pack(">Q", uid)) )
            )

def cao(tweet_json):
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
    sp = tweet['text'].encode('utf8').split('\n')
    text = "\\n".join(sp)
    #output.write( u"{}\t{}\t{}\t{}\t{}\n".format(
                        #tweet['id_str'],
                        #tweet['user']['id_str'],
                        #tweet['retweeted_status']['user']['id_str'] if tweet.has_key('retweeted_status') else "",
                        #ts,
                        #text.decode('utf8')
                    #).encode('utf8')
                #)
    load(   int(tweet['id_str'] ),
            int(tweet['user']['id_str'] ),
            int(ts ),
            text,
            tweet['retweeted_status']['user']['id_str'] if tweet.has_key('retweeted_status') else "",
        )


def gao(s3_path):

    filename = os.path.basename(s3_path)
    #subprocess.check_call(
            #"s3cmd get {0}".format(s3_path),
            #shell=True
            #)
    with open(filename, "r") as f:
        for line in f:
            if line.rstrip() != "":
                cao( line.rstrip() )

    #os.remove(filename )


with open("./json_files", "r") as f:
    for line in f:
        if line.rstrip() != "":
            gao(line.rstrip())

