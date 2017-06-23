#!/usr/bin/env python
import gzip
import json
import os
from processing.tokenizer import twokenize

stopwords = open('./resources/stop-word-list.txt', 'r').read().decode('utf-8').split('\r\n')

__author__ = 'cris'

class Tweet:

    @staticmethod
    def tokenizeTweetText(tweetText):
        return [t for t in twokenize.tokenize(tweetText.lower()) if t not in stopwords]

    @staticmethod
    def removeTabsInTweetText(tweetText):
        return tweetText.replace("\t", " ")

    @staticmethod
    def getHashtags(tweetText):
        # with repetitions
        tweetTokens = Tweet.tokenizeTweetText(tweetText)
        return [x for x in tweetTokens if x.startswith('#')]

    @staticmethod
    def getTweetAsDictionary(path):
        if os.path.isdir(path):
             for fname in os.listdir(path):
                for line in gzip.open(os.path.join(path, fname)):
                    try:
                        tweet = json.loads(line)
                    except:
                        print "Couldn't parse tweet: ", line[:200]
                    yield tweet, fname
        else:
            print "Opening file: ", path
            for line in gzip.open(path):
                try:
                    tweet = json.loads(line)
                except:
                    print "Couldn't parse tweet: ", line[:200]
                yield tweet


    @staticmethod
    def getTweetAsDictionaryNoGZ(path):
        if os.path.isdir(path):
             for fname in os.listdir(path):
                for line in open(os.path.join(path, fname)):
                    try:
                        tweet = json.loads(line)
                    except:
                        print "Couldn't parse tweet: ", line[:200]
                    yield tweet, fname
        else:
            print "Opening file: ", path
            for line in open(path):
                try:
                    tweet = json.loads(line)
                except:
                    print "Couldn't parse tweet: ", line[:200]
                yield tweet
