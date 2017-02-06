import codecs
import json
import logging
import os
import sys
from collections import defaultdict
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from twitter.Tweet import Tweet


def loadHashtags():
    htDict = defaultdict(list)
    with open("../filter/kw.txt") as f:
        for line in f:
            htType = line.split(":")[0]
            hashtagsString = line.split(":")[1].replace("\n", "")
            hashtags = hashtagsString.replace("\'", "").replace(" ", "").split(",")
            htDict[htType].extend(hashtags)
            htDict["All"].extend(hashtags)
    return htDict


def filterRelevance(allHtList, tweet):
    tweetDict = dict()
    tweetText = tweet["text"]

    if any(token in allHtList for token in tweetText):
        return tweet
    else:
        return None


def dumpDictValuesToFile(dict, file):
    line = json.dumps(dict) + "\n"
    file.write(line)


if __name__ == '__main__':
    logger = logging.getLogger("filterFoodKW.py")
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s;%(levelname)s;%(message)s")

    if len(sys.argv) != 5:
        print "You need to pass the following 4 params: <jsonTweetsFile> <filteredTweetsFile>"
        sys.exit(-1)
    inputFile = sys.argv[1]
    outputRelevant = codecs.open(sys.argv[2], "w", "utf-8")

    htDict = loadHashtags()
    print htDict
    tweetsAsDict = Tweet.getTweetAsDictionary(inputFile)

    i = 0
    for tweet in tweetsAsDict:
        if filterRelevance(htDict,tweet) is not None:
            dumpDictValuesToFile(tweet,outputRelevant)

    outputRelevant.close()

