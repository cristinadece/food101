"""

"""
# food101 : preprocess_tweet.py
# Created by muntean on 5/15/17
import json
import time
import requests
from datetime import datetime
from processing.load_keyword_dicts import loadCategoryDict
from processing.location.locations import Cities, Countries
from processing.location.get_location_from_tweet import getUserLocation, inferCountryFromCity, getLocationData, \
    getFinalUserLocation


citiesIndex, citiesInfo = Cities.loadFromFile()
countriesIndex, countriesInfo = Countries.loadFromFile()
ccDict = Countries.countryCodeDict(countriesInfo)
categoryDict = loadCategoryDict()


def get_media_url(tweet):
    """
    Checks if the tweets has media file attached
    :param tweet:
    :return:
    """
    if "entities" in tweet:
        if "media" in tweet["entities"]:
            foundMedia = tweet["entities"]["media"]
            return foundMedia[0]["media_url"]
        else:
            return None
    else:
        return None


def get_image_categories(img_url):
    """
    Gets the food category for a given img url.
    :param img_url:
    :return: list of dicts!!!!
    """
    request_string = 'http://test.tripbuilder.isti.cnr.it:8080/FoodRecognition/services/IRServices/recognizeByURL?imgURL='
    res = requests.get(request_string + img_url)
    try:
        candidates = json.loads(res.text)["guessed"]
    except:
        print "Error! Couldn't parse json ", res.text
        return None
    return candidates


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

    return city, country, tweet_coords


def get_day_as_int(tweet):
    """
    Gtes the day from the created_at field as and int. e.g. 20170605
    :param tweet:
    :return:
    """
    day = int(time.strftime('%Y%m%d', time.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')))
    return day


def get_tweet_text_category(tweet, categoryDict):
    """
    We need to see if the n-grams in tweet text, no parsing
    :param tweet:
    :param categoryDict:
    :return:
    """
    categoryList = categoryDict.keys()
    categ = set([categoryDict[token] for token in categoryList if token in tweet["text"]])
    return categ


def process_tweet(tweet, forStream=True):
    """

    :param tweet:
    :param forStream:
    :return:
    """

    new_tweet = dict()
    new_tweet["id"] = tweet["id"]
    new_tweet["text"] = tweet["text"]
    new_tweet["username"] = tweet["user"]["screen_name"]


    # PLACE COORDS LOCATION
    city, country, tweet_coords = get_location(tweet)
    new_tweet["coords"] = tweet_coords
    if tweet["place"] is not None:
        if "bounding_box" in tweet["place"].keys():
            new_tweet["bounding_box"] = tweet["place"]["bounding_box"]
        else:
            new_tweet["bounding_box"] = None
    else:
        new_tweet["bounding_box"] = None
    new_tweet["city"] = city
    new_tweet["country"] = country

    if forStream:
        if (new_tweet["coords"] is None) and (new_tweet["bounding_box"] is None):
            return None
    else:
        if new_tweet["country"] is None:
            return None


    # IMAGE
    media_url = get_media_url(tweet)
    new_tweet["media_url"] = media_url
    new_tweet["img_flag"] = False
    if media_url is not None:
        # img_categories = get_image_categories(media_url)
        img_categories = []
        new_tweet["img_categories"] = img_categories
        new_tweet["img_flag"] = True
    else:
        new_tweet["img_categories"] = None
        new_tweet["img_flag"] = True


    # TEXT
    text_categories = get_tweet_text_category(tweet, categoryDict)
    new_tweet["text_categories"] = text_categories

    if new_tweet["img_categories"] is None and len(new_tweet["text_categories"]) == 0:
        return None

    # DAY, DATE
    new_tweet["created_at_datetime"] = datetime.strptime(tweet["created_at"], '%a %b %d %H:%M:%S +0000 %Y')
    new_tweet["created_at_day"] = get_day_as_int(tweet)


    # INITIAL TWEET
    new_tweet["tweet_body"] = tweet

    return new_tweet

