"""
local-twitter

@autor: cristina muntean
@date: 23/06/16
"""

from elasticsearch import Elasticsearch
import os
import time
import requests
import argparse
from index.preprocess_tweet import get_media_url, get_food_category
from twitter.Tweet import Tweet
from location.get_location_from_tweet import *


parser = argparse.ArgumentParser(description='Import a dataset in light-svm format.')
parser.add_argument('-i', '--input', type=str, help='the input file')


def check_server_up():
    res = requests.get('http://foodmap.isti.cnr.it:9200', auth=('elastic', 'changeme'))
    print(res.content)

def setup():
    es = Elasticsearch(['localhost', 'otherhost'],
                       http_auth=('elastic', 'changeme'),
                       port=9200
                       )

    print "current dir: ", os.getcwd()
    os.chdir("/home/foodmap/food101/")
    print "current dir: ", os.getcwd()

    return es

def index_from_path(es, path):

    citiesIndex, citiesInfo = Cities.loadFromFile()
    countriesIndex, countriesInfo = Countries.loadFromFile()
    ccDict = Countries.countryCodeDict(countriesInfo)

    tweetsAsDict = Tweet.getTweetAsDictionary(inputFile)
    i = 0
    countImg = 0
    countCategory = 0
    countPlace = 0

    for tweet in tweetsAsDict:
        i += 1
        hasImg = False
        hasCategory = False
        hasCountry = False

        # 1. has photo?
        if get_media_url(tweet) is not None:
            hasImg = True
            countImg += 1
        else:
            continue

        # 2. has food category?
        if get_food_category(tweet) is not None:
            hasCategory = True
            countCategory += 1
        else:
            continue

        # 3. has location? we need city and country; record 2 separate fields
        ## 3.1. check for place
        tweet_coords, tweet_place_city, tweet_place_country, tweet_place_country_code, user_loc = getLocationData(tweet)
        ## 3.2. check for user location
        if (tweet_place_country is None):
            user_cities, user_countries = getUserLocation(user_loc, citiesIndex, citiesInfo, countriesIndex,
                                                          countriesInfo)
            inferred_countries = inferCountryFromCity(user_cities, citiesIndex, citiesInfo, ccDict)
            city, country = getFinalUserLocation(user_cities, user_countries, inferred_countries)
        else:
            city = tweet_place_city
            country = tweet_place_country

        if (tweet_place_country is not None) or (country is not None):
            hasCountry = True
            countPlace += 1

        # 4. extract date.day as int
        day = int(time.strftime('%Y%m%d', time.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')))

        # 5. extract tweet_id as long!
        tweet_id = tweet["id"]

        # SEE if CONDITIONS are met -> add to index
        if hasImg and hasCategory and hasCountry:
            tweet_dict = dict()
            tweet_dict["day"] = day
            tweet_dict["img_category"] = get_food_category(tweet)
            tweet_dict["city"] = city
            tweet_dict["country"] = country
            tweet_dict["tweet_body"] = tweet

            es.index(index='trends', doc_type='tweet', id=tweet_id, body=tweet_dict)

    print "Total relevant tweets in a day: ", i
    print "Tweets with media", countImg
    print "Tweets with category", countCategory
    print "Tweets with place", countPlace


def query_tweet_text(es, query):
    es.search(index="trends", body={"query": {"match": {'tweet_body.text': 'lasagna'}}})


def query_by_tweet_id(es, tweet_id):
    es.get(index='trends', doc_type='tweet', id=855919564705673216)


if __name__ == '__main__':
    args = parser.parse_args()

    inputFile = "/home/foodmap/food-tweets-2017-04-23.json.gz"
    index_from_path(inputFile)
