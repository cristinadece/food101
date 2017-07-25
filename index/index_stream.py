#!/usr/bin/env python

'''
StreamBBTwitter : StreamListener
@euthor: Cristina Muntean (cristina.muntean@isti.cnr.it)
@date: 9/22/16
-----------------------------

https://apps.twitter.com/app/13516461   - StreamFood

Consider changing method from GET to POST, as explained here: https://dev.twitter.com/streaming/reference/post/statuses/filter

'''

import os
import sys

os.chdir("/home/foodmap/food101/")
sys.path.append(os.getcwd())
import logging
import time
from twython import TwythonRateLimitError
from processing.load_keyword_dicts import getStreamFilterKeywords
from index.Stream2Index import Stream2Index


#### PUT CONFIG HERE
CONSUMER_KEY = 'JzAQ0Y2GbBg900GENP444u24K'
CONSUMER_SECRET = '5Mu6TnLR2oC7G9Z87egRzJU2X8vV3mL17qI5jBkL75g3wuLi5c'
ACCESS_TOKEN = '308456550-i6JR7eJo8H0VfV1X0Ujg06YhL9rJOFD3Pgey3zbi'
ACCESS_TOKEN_SECRET = 'J2rY8MCjkDblQpI3LPCXtG7v6nNO7K3YOOZbTASUGiRni'

# Minimal time accepted between two Rate Limit Errors
TOO_SOON = 10
# Time to wait if we receive a Rate Limit Error too soon after a previous one
WAIT_SOME_MORE = 60

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def log(msg, id=None):
    if id is not None:
        logger.info('%s: %s' % (id, msg))
    else:
        logger.info('%s' % msg)


def filter():
    start = time.time()
    htString = getStreamFilterKeywords()
    stream = Stream2Index(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    try:
        # FILTER
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


if __name__ == '__main__':
    filter()
