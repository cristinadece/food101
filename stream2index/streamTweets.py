#!/usr/bin/env python
'''
StreamBBTwitter : StreamListener
@euthor: Cristina Muntean (cristina.muntean@isti.cnr.it)
@date: 9/22/16
-----------------------------

https://apps.twitter.com/app/13516461   - StreamFood

Consider changing method from GET to POST, as explained here: https://dev.twitter.com/streaming/reference/post/statuses/filter

'''

import logging
#import oauth2 as oauth
import time
from twython import TwythonRateLimitError
from Stream2Index import Stream2Index

#### PUT CONFIG HERE
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''

# Minimal time accepted between two Rate Limit Errors
TOO_SOON = 10
# Time to wait if we receive a Rate Limit Error too soon after a previous one
WAIT_SOME_MORE = 60

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def getKeywordsList():
    """
    from the kw.txt and from categories.txt - with some processing to it
    :return: a string a keywords separated by comma
    """
    htList = list()
    with open("../resources/kw.txt") as f:
        for line in f:
            ht = line.replace("\n", "")
            htList.append(ht)


    htCategoryList = list()
    with open("../resources/categories.txt") as g:
        for line in g:
            ht = "#" + line.lower().replace("\r\n", "").replace(" ", "")
            htCategoryList.append(ht)

    htString = ",".join(htList) + "," + ",".join(htCategoryList)
    return htString



def log(msg, id=None):
    if id is not None:
        logger.info('%s: %s' % (id, msg))
    else:
        logger.info('%s' % msg)


def filter():
    start = time.time()

    htString = getKeywordsList()

    stream = Stream2Index(CONSUMER_KEY, CONSUMER_SECRET,
                        ACCESS_TOKEN, ACCESS_TOKEN_SECRET, retry_in=3600)  # retry_in - n seconds
    try:
        # FILTER
        # stream.statuses.filter(track='#IF2016', locations=PISA)
        stream.statuses.filter(track=htString)
    except TwythonRateLimitError as e:
        # If this error is received after only few calls (10 seconds of calls) wait just a minute
        if time.time() - start < TOO_SOON:
            log('Waiting %s seconds more for resuming download after recurrent rate limit error ...'
                % WAIT_SOME_MORE)
            time.sleep(WAIT_SOME_MORE)
        else:
            log(e, id)
            log('Waiting %s seconds for resuming download after rate limit error ...')
            time.sleep(60)


def main():
    filter()


if __name__ == '__main__':
    main()