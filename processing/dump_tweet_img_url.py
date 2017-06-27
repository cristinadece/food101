"""

"""

import argparse
import os
import sys
os.chdir("/home/foodmap/food101/")
sys.path.append(os.getcwd())
from processing.load_keyword_dicts import loadCategoryDict
from processing.location.locations import Cities, Countries
from processing.location.get_location_from_tweet import getUserLocation, inferCountryFromCity, getLocationData, \
    getFinalUserLocation
from processing.twitter.Tweet import Tweet

citiesIndex, citiesInfo = Cities.loadFromFile()
countriesIndex, countriesInfo = Countries.loadFromFile()
ccDict = Countries.countryCodeDict(countriesInfo)
categoryDict = loadCategoryDict()

parser = argparse.ArgumentParser(description='Index tweets in trend index.')
parser.add_argument('-i', '--inputFile', type=str, help='the input file')
parser.add_argument('-o', '--outputFile', type=str, help='the output file')


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


def process_tweet(tweet):
    """

    :param tweet:
    :param forStream:
    :return:
    """
    s = ""
    s += tweet["id_str"]
    # PLACE COORDS LOCATION
    city, country, tweet_coords = get_location(tweet)

    if country is None:
        return "nocountry"
    else:
        # IMAGE
        media_url = get_media_url(tweet)
        if media_url is not None:
            s += "\t" + media_url + "\n"
            return s
        else:
            return "noimg"


if __name__ == '__main__':
    args = parser.parse_args()
    print args
    inputFile = args.inputFile
    outputFile = args.outputFile


    i = 0
    nocountry = 0
    noimg = 0
    tweetsAsDict = Tweet.getTweetAsDictionary(inputFile)

    with open(outputFile, "w") as f:
        for tweet in tweetsAsDict:
            i += 1
            line = process_tweet(tweet)
            if line in "nocountry":
                nocountry += 1
            elif line in "noimg":
                noimg += 1
            else:
                f.write(line)

    print "Total tweet: ", i
    print "Tweets without country: ", nocountry
    print "tweets with count but without img: ", noimg