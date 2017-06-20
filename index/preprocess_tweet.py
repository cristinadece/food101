"""

"""
# food101 : preprocess_tweet.py
# Created by muntean on 5/15/17
import json
import random
import time
import requests
from location.get_location_from_tweet import getUserLocation, inferCountryFromCity, getLocationData, \
    getFinalUserLocation
from location.locations import Cities, Countries

### SHOULD I DO THID here?
from twitter.Tweet import Tweet

citiesIndex, citiesInfo = Cities.loadFromFile()
countriesIndex, countriesInfo = Countries.loadFromFile()
ccDict = Countries.countryCodeDict(countriesInfo)


def get_media_url(tweet):
    """
    Checks if the tweets has media file attached
    :param tweet:
    :return:
    """
    if "media" in tweet["entities"]:
        foundMedia = tweet["entities"]["media"]
        return foundMedia[0]["media_url"]
    else:
        return None


def get_location(tweet):
    """
    Gets the location from the Place/GPS or user location
    :param tweet:
    :return:
    """
    tweet_coords, tweet_place_city, tweet_place_country, tweet_place_country_code, user_loc = getLocationData(tweet)

    if (tweet_place_country is None):
        user_cities, user_countries = getUserLocation(user_loc, citiesIndex, citiesInfo, countriesIndex, countriesInfo)
        inferred_countries = inferCountryFromCity(user_cities, citiesIndex, citiesInfo, ccDict)
        city, country = getFinalUserLocation(user_cities, user_countries, inferred_countries)
    else:
        city = tweet_place_city
        country = tweet_place_country

    return city, country


def get_image_category(img_url):
    """
    Gets the food category for a given img url.
    :param img_url:
    :return:
    """
    request_string = 'http://test.tripbuilder.isti.cnr.it:8080/FoodRecognition/services/IRServices/recognizeByURL?imgURL='
    res = requests.get(request_string + img_url)
    candidates = json.loads(res.text)["guessed"]
    if len(candidates) != 0:
        category = candidates[0]["label"]
    else:
        category = None
    return category


def get_day_as_int(tweet):
    """
    Gtes the day from the created_at field as and int. e.g. 20170605
    :param tweet:
    :return:
    """
    day = int(time.strftime('%Y%m%d', time.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')))
    return day


def loadCartegoryList():
    """

    :return:
    """
    htCategoryList = list()
    with open("./resources/categories.txt") as g:
        for line in g:
            ht = "#" + line.lower().replace("\r\n", "").replace(" ", "")
            htCategoryList.append(ht)
    return htCategoryList


def get_tweet_text_category(tweet, categoryList):
    """

    :param tweet:
    :param categoryList:
    :return:
    """
    tweetTextTokens = Tweet.tokenizeTweetText(tweet["text"])
    categ = [token for token in tweetTextTokens if token in categoryList]
    return categ  #todo, make some tests


def enrich_tweet_trend(tweet):
    """

    :param tweet:
    :return:
    """
    media_url = get_media_url(tweet)
    tweet["media_url"] = media_url
    if media_url is not None:
        img_category = get_image_category(media_url)
        tweet["img_category"] = img_category
    else:
        tweet["img_category"] = None
    city, country = get_location(tweet)
    tweet["city"] = city
    tweet["country"] = country
    return tweet


def enrich_tweet_stream(tweet):
    """

    :param tweet:
    :return:
    """
    media_url = get_media_url(tweet)
    tweet["media_url"] = media_url
    if media_url is not None:
        img_category = get_image_category(media_url)
        tweet["img_category"] = img_category
    else:
        tweet["img_category"] = None

    # longitude first, then latitude
    # longitude first, then latitude
    if tweet["coordinates"] is not None:
        tweet["coordinates"] = tweet['coordinates']['coordinates']  # returns a list [longitude, latitude]
    else:
        tweet["coordinates"] = None

    if tweet["place"] is not None:
        if "bounding_box" in tweet["place"].keys():
            tweet["bounding_box"] = tweet["place"]["bounding_box"]
        else:
            tweet["bounding_box"] = None
    else:
        tweet["bounding_box"] = None
    return tweet


def get_tweet_snippet(tweet):
    """
    Reduce tweet to a snippet!
    :param tweet:
    :return:
    """
    stream_dict = dict()
    stream_dict["id"] = tweet["id"]
    stream_dict["day"] = get_day_as_int(tweet)
    stream_dict["media_url"] = tweet["media_url"]
    stream_dict["img_category"] = tweet["img_category"]
    stream_dict["text"] = tweet["text"]
    stream_dict["created_at"] = tweet["created_at"]  # put this as datetime!!!!
    # ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
    stream_dict["username"] = tweet["user"]["screen_name"]
    stream_dict["coordinates"] = tweet["coordinates"]
    stream_dict["bounding_box"] = tweet["bounding_box"]
    return stream_dict

