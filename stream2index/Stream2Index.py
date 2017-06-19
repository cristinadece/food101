#!/usr/bin/env python
'''
StreamBBTwitter : MyStreamer
@euthor: Cristina Muntean (cristina.muntean@isti.cnr.it)
@date: 9/22/16
-----------------------------
 or here: http://www.kalisch.biz/2013/10/harvesting-twitter-with-python/

'''

import json
from twython import TwythonStreamer
from elasticsearch import Elasticsearch
from index.preprocess_tweet import enrich_tweet, get_tweet_snippet


def isValid(enriched_tweet):
    hasImg = False
    hasCategory = False
    hasCountry = False

    if enriched_tweet["media_url"] is not None:
        hasImg = True
    if enriched_tweet["img_category"] is not None:
        hasCategory = True
    if enriched_tweet["country"] is not None:
        hasCountry = True

    if hasImg and hasCategory and hasCountry:
        return True
    else:
        return False


class Stream2Index(TwythonStreamer):

    es = Elasticsearch(['localhost', 'otherhost'],
                           http_auth=('elastic', 'changeme'),
                           port=9200
                           )


    def on_success(self, data):
        enriched_tweet = enrich_tweet(data)
        if isValid(enriched_tweet):
            tweet_snippet = get_tweet_snippet(enriched_tweet)
            es.index(index='stream', doc_type='tweet_snippet', id=tweet_snippet["id"], body=tweet_snippet)
            print "Indexed tweet: ", tweet["id"]

    def on_error(self, status_code):
        print status_code



