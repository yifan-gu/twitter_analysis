#!/usr/bin/env python

import json
import re

# objective
#   created_at: timestamp
#   tweet id:
#   text:


def chaogao(tweet_json):
    #print tweet_json
    tweet = json.loads(tweet_json)
    #text  = (repr(tweet['text']))
    #if(text[0] == 'u'):
        #text = text[2:-1]
    #text = text.replace('/','\\/')
    i = tweet_json.find("text\":\"") + 7
    pattern = re.compile(r'[^\\]"')
    m = pattern.search(tweet_json, i)
    j = m.end()-1
    text = tweet_json[i:j]
    print "{}:{}".format(tweet['id'], text)
    #print ""

def gao(f):
    for line in f:
        if line.strip() != "":
            chaogao(line.rstrip())

gao(open('small.json', "r"))
