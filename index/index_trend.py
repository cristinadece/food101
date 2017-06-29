"""
local-twitter

@autor: cristina muntean
@date: 23/06/16
"""

import argparse
import json
import os
import sys

import time

os.chdir("/home/foodmap/food101/")
sys.path.append(os.getcwd())
import requests
from elasticsearch import Elasticsearch, RequestError
from processing.preprocess_tweet import process_tweet
from processing.twitter.Tweet import Tweet

parser = argparse.ArgumentParser(description='Index tweets in trend index.')
parser.add_argument('-f', '--inputFile', type=str, help='the input file')
parser.add_argument('-i', '--indexName', type=str, help='the index name')



def setup(indexName):
    """
    Create the index in case it doesn't exist.
    If it exists then we ignore the error message : status 400
    :return:
    """
    es = Elasticsearch(['localhost'],  # 146.48.82.85
                            http_auth=('elastic', 'changeme'),
                            port=9200
                            )
    mapping = json.load(open("./containers/index/mapping.json"))
    print es.indices.create(indexName, ignore=400, body=mapping)
    return es


def index_from_path(es, inputFile, indexName):
    """
    We index tweet from file

    :param es: the ES instance
    :param inputFile: the .gz file to read and index from
    :return:

    Possible errors:
    - elasticsearch.exceptions.RequestError: TransportError(400, u'mapper_parsing_exception',
    u'failed to parse [bounding_box]')

    - elasticsearch.exceptions.ConnectionTimeout: ConnectionTimeout caused by -
    ReadTimeoutError(HTTPConnectionPool(host=u'localhost', port=9200): Read timed out. (read timeout=10))

    - elasticsearch.exceptions.ConnectionError: ConnectionError(('Connection aborted.', error(104,
    'Connection reset by peer'))) caused by: ProtocolError(('Connection aborted.',
    error(104, 'Connection reset by peer')))
    """
    tweetsAsDict = Tweet.getTweetAsDictionary(inputFile)
    i = 0
    numIndex = 0
    for tweet in tweetsAsDict:
        i += 1
        if i % 10000 == 0:
            print "Processed tweets: ", i
            print "Indexed tweets: ", numIndex

        new_tweet = process_tweet(tweet, forStream=False)
        if new_tweet is None:
            continue

        try:
            es.index(index=indexName, doc_type='tweet', id=new_tweet["id"], body=new_tweet)
            numIndex += 1
            print "Indexed tweet: ", new_tweet["id"]
        except RequestError as e:
            print "Couldn't index tweet id: ", new_tweet["id"]
            print e.status_code, e.message
            time.sleep(60)

    print "Processed tweets: ", i
    print "Indexed tweets: ", numIndex


if __name__ == '__main__':
    args = parser.parse_args()
    print args
    inputFile = args.inputFile
    indexName = args.indexName
    es = setup(indexName)
    index_from_path(es, inputFile, indexName)
