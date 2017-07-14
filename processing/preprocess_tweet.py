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
    getFinalUserLocation, inferCountryByGeolocation, hasGeoInformation
from processing.twitter.Tweet import Tweet

citiesIndex, citiesInfo = Cities.loadFromFile()
countriesIndex, countriesInfo = Countries.loadFromFile()
ccDict = Countries.countryCodeDict(countriesInfo)
categoryDict = loadCategoryDict()
countries_geojson = Countries.loadGeoJsonCountries()




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
    country = None
    city = None
    
    if not hasGeoInformation(tweet):
        # user_loc = getUserLocationProfile(tweet)
        user_cities, user_countries = getUserLocation(user_loc, citiesIndex, citiesInfo, countriesIndex, countriesInfo)
        inferred_countries = inferCountryFromCity(user_cities, citiesIndex, citiesInfo, ccDict)
        city, country = getFinalUserLocation(user_cities, user_countries, inferred_countries)
    else:
        # city = tweet_place_city
        # country = tweet_place_country
        #### TODO Vinicius
        ## Use coord and BB to detect country
        city = None
        country = inferCountryByGeolocation(tweet, countries_geojson)

    return city, country, tweet_coords


def get_day_as_int(tweet):
    """
    Gtes the day from the created_at field as and int. e.g. 20170605
    :param tweet:
    :return:
    """
    day = int(time.strftime('%Y%m%d', time.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')))
    return day

def get_month_as_int(tweet):
    """
    Gtes the day from the created_at field as and int. e.g. 20170605
    :param tweet:
    :return:
    """
    month = int(time.strftime('%Y%m', time.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y'))+"01")
    return month


def get_tweet_text_category(tweet, categoryDict):
    """
    We need to see if the n-grams in tweet text, no parsing
    :param tweet:
    :param categoryDict:
    :return:
    """
    categoryList = categoryDict.keys()
    tokenList = Tweet.tokenizeTweetText(tweet["text"])
    categ = set([categoryDict[token] for token in tokenList if token in categoryList])
    return categ


def get_img_class_from_file(tweet, tweetImgCategoryDict):
    """

    :param tweet:
    :param tweetImgCategoryDict:
    :return:
    """
    result = list()
    catDict = dict()

    info = tweetImgCategoryDict[tweet["id"]]
    catDict["score"] = info[1]
    catDict["label"] = info[0]
    result.append(catDict)

    tweet["img_flag"] = True
    tweet["img_categories"] = result

    return tweet


def process_tweet(tweet, forStream=True):
    """

    :param tweet:
    :param forStream:
    :return:
    """

    new_tweet = dict()
    if "id" not in tweet:
        return None
    new_tweet["id"] = tweet["id"]
    new_tweet["id_str"] = tweet["id_str"]
    new_tweet["timestamp_ms"] = tweet["timestamp_ms"]
    new_tweet["text"] = tweet["text"]
    new_tweet["username"] = tweet["user"]["screen_name"]
    new_tweet["lang"] = tweet["lang"]
    new_tweet["hashtags"] = Tweet.getHashtags(tweet["text"])

    # print new_tweet['text']
    # print tweet["entities"]["media"][0]["media_url"]


    # PLACE COORDS LOCATION
    """
    In GeoJSON, and therefore Elasticsearch, the correct coordinate order is longitude, latitude (X, Y) within 
    coordinate arrays. This differs from many Geospatial APIs (e.g., Google Maps) that generally use the colloquial 
    latitude, longitude (Y, X).
    """
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
        # WE NEED TO CLASSIFY for stream
        if forStream == True:
            img_categories = get_image_categories(media_url)
            new_tweet["img_categories"] = img_categories
            new_tweet["img_flag"] = True
        # THIS IS THE TREND INDEX, we do batch img classif
        else:
            img_categories = []
            new_tweet["img_categories"] = img_categories
            new_tweet["img_flag"] = False  # todo when we use the classifier we must change this to True
    else:
        new_tweet["img_categories"] = None
        new_tweet["img_flag"] = True


    # TEXT
    text_categories = get_tweet_text_category(tweet, categoryDict)
    new_tweet["text_categories"] = list(text_categories)

    hasNoImgCateg = (new_tweet["img_categories"] is None) or (len(new_tweet["img_categories"]) == 0)
    if hasNoImgCateg and len(new_tweet["text_categories"]) == 0:
        return None

    # DAY, DATE
    new_tweet["created_at_datetime"] = datetime.strptime(tweet["created_at"], '%a %b %d %H:%M:%S +0000 %Y')
    new_tweet["created_at_day"] = get_day_as_int(tweet)
    new_tweet["created_at_month"] = get_month_as_int(tweet)

    return new_tweet




# {u'_score': 1.0, u'_type': u'tweet', u'_id': u'840207017071529985', u'_source': {u'username': u'FairhavenTours',
#  u'lang': u'en', u'text_categories': [u'ice cream'], u'city': u'fairhaven', u'text': u'Ice Cream is coming to Pink Bonnet.
# #Fairhaven #Bakery #IceCream https://t.co/dXKtTBVnbR', u'img_categories': None, u'hashtags': [u'#fairhaven',
# u'#bakery', u'#icecream'], u'img_flag': True, u'timestamp_ms': u'1489155937818', u'bounding_box': None, u'coords': None,
#  u'id_str': u'840207017071529985', u'country': u'united states', u'id': 840207017071529985, u'created_at_day': 20170310,
#  u'created_at_datetime': u'2017-03-10T14:25:37', u'media_url': None}, u'_index': u'trend'}

# {u'_score': 1.0, u'_type': u'tweet', u'_id': u'840207241076699136', u'_source': {u'username': u'recipesprep',
# u'lang': u'en', u'text_categories': [u'cheesecake'], u'city': None, u'text': u'#Food #Pastry-Bites #food
# https://t.co/wNqtCpuvDH #Amazing #Strawberry #Cheesecake Pastry Bites https://t.co/rfQ7bOKCaB', u'img_categories': [],
# u'hashtags': [u'#food', u'#pastry-bites', u'#food', u'#amazing', u'#strawberry', u'#cheesecake'], u'img_flag': False,
# u'timestamp_ms': u'1489155991225', u'bounding_box': None, u'coords': None, u'id_str': u'840207241076699136',
# u'country': u'canada', u'id': 840207241076699136, u'created_at_day': 20170310, u'created_at_datetime': u'2017-03-10T14:26:31',
# u'media_url': u'http://pbs.twimg.com/media/C6kECFvWkAA3JH5.jpg'}, u'_index': u'trend'}
