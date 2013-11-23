#!/usr/bin/env python

import sys,os
import struct

def barr2str(arr):
    return "\\x" + "\\x".join("{:02x}".format(ord(i)) for i in arr)

ts_output = open('hb_ts', "w")
ud_output = open('hb_uid', "w")
rt_output = open('hb_rt', "w")

def load(line):
    tweet = line.split('\t', 4)

    tid    = int(tweet[0])
    uid    = int(tweet[1])
    ts     = int(tweet[3])
    tx     = tweet[4]

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

    if tweet[2] == "":
        return

    rt_uid = int(tweet[2])

    rt_output.write(
            # put retweet, rt_uid, tweet:tw_id, uid
            'put "retweet", "{}", "tweet:{}","{}"\n'.format(
                barr2str(struct.pack(">Q", rt_uid)),
                barr2str(struct.pack(">Q", tid)),
                barr2str(struct.pack(">Q", uid)) )
            )



with open("sample_output","r") as f:
    for line in f:
        load(line.rstrip())
