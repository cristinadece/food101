#!/usr/bin/env python
'''
StreamBBTwitter : MyStreamer
@euthor: Cristina Muntean (cristina.muntean@isti.cnr.it)
@date: 28/06/17
-----------------------------
 or here: http://www.kalisch.biz/2013/10/harvesting-twitter-with-python/

'''
import json
import os
import sys
import time
os.chdir("/home/foodmap/food101/")
sys.path.append(os.getcwd())
print os.getcwd()
from twython import TwythonStreamer
from elasticsearch import Elasticsearch, RequestError
from processing.preprocess_tweet import process_tweet, process_tweet_special


class Stream2Index(TwythonStreamer):
    """


    """
    def __init__(self, CONSUMER_KEY, CONSUMER_SECRET,
                 ACCESS_TOKEN, ACCESS_TOKEN_SECRET):
        super(Stream2Index, self).__init__(app_key=CONSUMER_KEY, app_secret=CONSUMER_SECRET, oauth_token=ACCESS_TOKEN,
                                           oauth_token_secret=ACCESS_TOKEN_SECRET, retry_in=3600)

        self.es = Elasticsearch(['localhost'],  #146.48.82.85
                                http_auth=('elastic', 'changeme'),
                                port=9200
                                )
        # mapping = json.load(open("./containers/index/mapping.json"))
        print self.es.indices.create("stream", ignore=400) #, body=mapping)

    def on_success(self, data):
        if "#foodsigir2017" in data["text"]:
            print "is sigir tweet", data["id"]
            new_tweet = process_tweet_special(data)
        else:
            new_tweet = process_tweet(data, forStream=True)
        if new_tweet is not None:
            try:
                self.es.index(index='stream', doc_type='tweet', id=new_tweet["id"], body=new_tweet)
                print "Indexed tweet: ", new_tweet["id"]
            except RequestError as e:
                print "Couldn't index tweet id: ", new_tweet["id"]
                print e.status_code, e.message
                # todo check error when not parsing bounding box geo-shape
                time.sleep(60)

    def on_error(self, status_code):
        print status_code



