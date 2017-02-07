import codecs
import json
import logging
import os
import sys
from collections import defaultdict
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from twitter.Tweet import Tweet


def loadHashtags():
    htList = list()
    with open("../filter/kw.txt") as f:
        for line in f:
            ht = line.replace("\n", "")
            htList.append(ht)
    return htList


def filterRelevance(allHtList, tweet):
    tweetText = tweet["text"]

    for ht in allHtList:
	if ht in tweetText:
            return tweet
    
    return None


def dumpDictValuesToFile(dict, file):
    line = json.dumps(dict) + "\n"
    file.write(line)


if __name__ == '__main__':
    logger = logging.getLogger("filterFoodKW.py")
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s;%(levelname)s;%(message)s")

    if len(sys.argv) != 3:
        print "You need to pass the following 4 params: <jsonTweetsFile> <filteredTweetsFile>"
        sys.exit(-1)
    inputFile = sys.argv[1]
    outputRelevant = codecs.open(sys.argv[2], "w", "utf-8")

    htList = loadHashtags()
    tweetsAsDict = Tweet.getTweetAsDictionary(inputFile)

    i = 0
    for tweet in tweetsAsDict:
        if filterRelevance(htList,tweet) is not None:
            dumpDictValuesToFile(tweet,outputRelevant)

    outputRelevant.close()

