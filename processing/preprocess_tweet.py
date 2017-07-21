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
    if candidates[0]["score"] >= 7.0:
        return candidates
    else:
        return []


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
        country = None
        try:
            country = inferCountryByGeolocation(tweet, countries_geojson)
        except:
            print "Couldn't infer country for ", tweet


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

    if tweet["id"] in tweetImgCategoryDict:
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
        # THIS IS THE TREND INDEX, we do batch img classif at a next step
        else:
            img_categories = get_image_categories(media_url)
            new_tweet["img_categories"] = img_categories
            new_tweet["img_flag"] = True  # todo when we use the classifier we must change this to True
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



def process_tweet_special(tweet):
    """
    This is only for stream for tweets containing #foodsigir2017
    :param tweet:
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


    if (new_tweet["coords"] is None) and (new_tweet["bounding_box"] is None):
        new_tweet["bounding_box"] = {"type": "Polygon", "coordinates": [[[139.68794345855713, 35.66782614259895],
                [139.68760013580322, 35.662073226633424], [139.69326496124268, 35.65408818971974],
                [139.69918727874756, 35.64871789058102], [139.70167636871338, 35.64763681268489],
                [139.7023630142212, 35.64673009091096], [139.70725536346436, 35.6462069775141],
                [139.711332321167, 35.64903174916549], [139.7127056121826, 35.64854352416794],
                [139.71467971801755, 35.64840403076344], [139.71862792968747, 35.64892712977434],
                [139.71961498260498, 35.64871789058102], [139.72034454345703, 35.64826453711539],
                [139.72304821014404, 35.64763681268489], [139.72463607788086, 35.64673009091096],
                [139.7282838821411, 35.646869587238285], [139.73266124725342, 35.64739269629656],
                [139.7356653213501, 35.646590594340026], [139.73618030548096, 35.64693933531064],
                [139.73673820495605, 35.64882251024618], [139.73669528961182, 35.65112410821579],
                [139.7365665435791, 35.652728213038685], [139.73716735839844, 35.656215286299144],
                [139.73648071289062, 35.65767981166863], [139.73708152770996, 35.66012062760205],
                [139.73776817321777, 35.66113180091841], [139.7426176071167, 35.6596324703837],
                [139.74390506744385, 35.661829154365705], [139.74514961242676, 35.66336331051176],
                [139.74729537963867, 35.66189888937547], [139.7494411468506, 35.66172455173687],
                [139.7513723373413, 35.66106206523872], [139.75510597229004, 35.66032983692497],
                [139.76102828979492, 35.66733803249021], [139.7625732421875, 35.66660586173127],
                [139.7669506072998, 35.66967396097516], [139.7721004486084, 35.67577494427893],
                [139.77572679519653, 35.68170116720479], [139.77104902267456, 35.68360095138859],
                [139.76126432418823, 35.68565754749378], [139.75581407546997, 35.67730883242672],
                [139.75399017333984, 35.67814548626268], [139.74969863891602, 35.67716938926793],
                [139.74703788757324, 35.67995820614855], [139.73716735839844, 35.678912411239935],
                [139.73098754882812, 35.675077712647415], [139.72540855407715, 35.673264881898525],
                [139.71656799316406, 35.669865713262666], [139.7124695777893, 35.66519379916189],
                [139.70298528671265, 35.66951707239733], [139.69995975494385, 35.66847114066505],
                [139.69367265701294, 35.66826195267408], [139.69180583953857, 35.66782614259895],
                [139.68794345855713, 35.66782614259895]]]}
        new_tweet["city"] = "tokyo"
        new_tweet["country"] = "japan"

    # IMAGE
    media_url = get_media_url(tweet)
    new_tweet["media_url"] = media_url
    new_tweet["img_flag"] = False
    if media_url is not None:
        # WE NEED TO CLASSIFY for stream
        img_categories = get_image_categories(media_url)
        new_tweet["img_categories"] = img_categories
        new_tweet["img_flag"] = True
    else:
        new_tweet["img_categories"] = None
        new_tweet["img_flag"] = True


    # TEXT
    text_categories = get_tweet_text_category(tweet, categoryDict)
    new_tweet["text_categories"] = list(text_categories)

    hasNoImgCateg = (new_tweet["img_categories"] is None) or (len(new_tweet["img_categories"]) == 0)
    if hasNoImgCateg and len(new_tweet["text_categories"]) == 0:
        new_tweet["img_categories"] = list()
        catDict = dict()
        catDict["score"] = 0.0
        catDict["label"] = "unknown"
        new_tweet["img_categories"].append(catDict)
        new_tweet["img_flag"] = True

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
