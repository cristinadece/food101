"""
This is a script which filter tweets containing certain keywords which are food related.
"""

import codecs
import argparse
import json
import logging
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from twitter.Tweet import Tweet

parser = argparse.ArgumentParser(description='<ix two files with frequencies to discover local topics')
parser.add_argument('--input', '-inputFile', help='the file or directory where we find the raw tweets')
parser.add_argument('--output', '-outputFile', help='the output file continuing only the filtered tweets')


def loadHashtags():
    """
    Loads hashtags from hardcoded file.
    :return: a list of hashtags
    """
    htList = list()
    with open("../resources/kw.txt") as f:
        for line in f:
            ht = line.replace("\n", "")
            htList.append(ht)
    return htList


def filterRelevance(allHtList, tweet):
    """
    We filter tweets which contain hashtags from the loaded list
    :param allHtList:
    :param tweet:
    :return: a tweets if
    """
    tweetText = tweet["text"]

    for ht in allHtList:
        if ht in tweetText:
            return tweet

    return None


def dumpDictValuesToFile(dict, file):
    """
    Print utility UTF8, also covers ascii error
    :param dict:
    :param file:
    :return:
    """
    line = json.dumps(dict) + "\n"
    file.write(line)


if __name__ == '__main__':
    logger = logging.getLogger("filterFoodKW.py")
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s;%(levelname)s;%(message)s")

    args = parser.parse_args()
    print args

    inputFile = args.input
    outputFile = args.output
    outputWriter = codecs.open(outputFile, "w", "utf-8")

    htList = loadHashtags()
    tweetsAsDict = Tweet.getTweetAsDictionary(inputFile)

    for tweet in tweetsAsDict:
        if filterRelevance(htList, tweet) is not None:
            dumpDictValuesToFile(tweet, outputWriter)
    outputWriter.close()
