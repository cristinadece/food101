#!/usr/bin/env python
import gzip
import json
import os
from tokenizer import twokenize

#stopwords=open('../resources/stop-word-list.txt', 'r').read().decode('utf-8').split('\r\n')

dir = os.path.dirname(__file__)
stopwordsFile = os.path.join(dir, '../resources/stop-word-list.txt')
stopwords = open(stopwordsFile, 'r').read().decode('utf-8').split('\r\n')

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
    def getTweetAsTweetTextTokens(path):

        if os.path.isdir(path):
            for fname in os.listdir(path):
                for line in gzip.open(os.path.join(path, fname)):
                    try:
                        tweet = json.loads(line)
                    except:
                        print "Couldn't parse tweet: ", line[:200]

                    tweetText = tweet['text']
                    tokenList = Tweet.tokenizeTweetText(tweetText)
                    yield tokenList
        else:  #this means it is a file
            for line in gzip.open(path):
                    try:
                        tweet = json.loads(line)
                    except:
                        print "Couldn't parse tweet: ", line[:200]

                    tweetText = tweet['text']
                    tokenList = Tweet.tokenizeTweetText(tweetText)
                    yield tokenList

    @staticmethod
    def getTweetAsTweetTextTokensNoGZ(path):

        if os.path.isdir(path):
            for fname in os.listdir(path):
                for line in open(os.path.join(path, fname)):
                    try:
                        tweet = json.loads(line)
                    except:
                        print "Couldn't parse tweet: ", line[:200]

                    tweetText = tweet['text']
                    tokenList = Tweet.tokenizeTweetText(tweetText)
                    yield tokenList
        else:  # this means it is a file
            for line in open(path):
                try:
                    tweet = json.loads(line)
                except:
                    print "Couldn't parse tweet: ", line[:200]

                tweetText = tweet['text']
                tokenList = Tweet.tokenizeTweetText(tweetText)
                yield tokenList


    @staticmethod
    def getTweetAsDictionary(path):
        if os.path.isdir(path):
             for fname in os.listdir(path):
                for line in gzip.open(os.path.join(path, fname)):
                    try:
                        tweet = json.loads(line)
                    except:
                        print "Couldn't parse tweet: ", line[:200]
                    yield tweet
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


if __name__ == '__main__':
    #print stopwords

    j = 0
    for i in Tweet.getTweetAsDictionary("../../../english-tweets/english-tweets-20150901.json.part.gz"):

        j += 1

        if i['place']!=None:
            print i["place"]

        if i['coordinates']!=None:
            print i['coordinates']["coordinates"]

        if j % 1000 == 0:
            break


