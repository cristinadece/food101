"""
local-twitter

@autor: cristina muntean
@date: 23/06/16
"""

import argparse
import os
os.chdir("/home/foodmap/food101/")
import requests
from elasticsearch import Elasticsearch
from processing.preprocess_tweet import process_tweet
from processing.twitter.Tweet import Tweet

parser = argparse.ArgumentParser(description='Index tweets in trend index.')
parser.add_argument('-f', '--inputFile', type=str, help='the input file')
parser.add_argument('-i', '--indexName', type=str, help='the input file')


def check_server_up():
    """

    :return:
    """
    res = requests.get('http://foodmap.isti.cnr.it:9200', auth=('elastic', 'changeme'))
    print(res.content)


def setup():
    """

    :return:
    """
    es = Elasticsearch(['localhost', 'otherhost'],
                       http_auth=('elastic', 'changeme'),
                       port=9200
                       )

    return es


def index_from_path(es, inputFile, indexName):
    """

    :param es:
    :param inputFile:
    :return:
    """
    tweetsAsDict = Tweet.getTweetAsDictionary(inputFile)
    i = 0
    numIndex = 0
    for tweet in tweetsAsDict:
        i += 1
        if i % 10000 ==0:
            print "Processed tweets: ", i
            print "Indexed tweets: ", numIndex

        new_tweet = process_tweet(tweet, forStream=False)
        if new_tweet is None:
            continue
        new_tweet_id = new_tweet["id"]

        # check len of img_categ
        if len(new_tweet["img_categories"]) != 0:
            new_tweet["img_category"] = new_tweet["img_categories"][0]["label"]
            new_tweet["img_category_score"] = new_tweet["img_categories"][0]["score"]
        else:
            new_tweet["img_category"] = None
            new_tweet["img_category_score"] = 0.0



        # check len of text_categ
        if len(new_tweet["text_categories"]) != 0:
            for cat in new_tweet["text_categories"]:
                new_tweet["text_category"] = cat

                # split index per month
                es.index(index=indexName, doc_type='tweet', id=new_tweet_id, body=new_tweet)
                numIndex += 1
        else:
            new_tweet["text_category"] = None
            # split index per month
            es.index(index=indexName, doc_type='tweet', id=new_tweet_id, body=new_tweet)
            numIndex += 1
    print "Total relevant tweets in a day: ", i


if __name__ == '__main__':
    args = parser.parse_args()
    print args
    inputFile = args.f
    indexName = args.i
    index_from_path(inputFile, indexName)
