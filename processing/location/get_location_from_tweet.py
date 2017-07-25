"""
Some utilities for finding city and country from the user_location field
"""
# food101 : get_place_from_user_location
# Created by muntean on 4/26/17
from processing.tokenizer import twokenize, ngrams
from shapely.geometry import shape


def getLocationsFromToken(token, citiesIndex, citiesInfo, countriesIndex, countriesInfo):
    """
    From a token, with the help of the dictionary tries to establish a city and/or country
    :param token: a string
    :param citiesIndex: 
    :param citiesInfo: 
    :param countriesIndex: 
    :param countriesInfo: 
    :return: city, country
    """
    city = ""
    country = ""

    #if citiesIndex[token] and len(citiesIndex[token])==1: #TODO: this condition is because we have more cities with same name
    if citiesIndex[token]:
        geonamesidCity = citiesIndex[token][0]
        city = citiesInfo[geonamesidCity][0]
    if countriesIndex[token]:
        geonamesidCountry = countriesIndex[token][0]
        country = countriesInfo[geonamesidCountry][0]  # we take the name of the country from the tuple, elim. both UK and United K.

    if (citiesIndex[token]) and (countriesIndex[token]): # todo: this never returns a city named after a country
        city = ""

    return city, country


def cleanSets(potentialCities, potentialCountries):
    """
    Cleans the lists of empty strings
    :param potentialCities: 
    :param potentialCountries: 
    :return: potentialCities, potentialCountries
    """
    if "" in potentialCities:
        potentialCities.remove("")
    if "" in potentialCountries:
        potentialCountries.remove("")
    return potentialCities, potentialCountries


def inferCountryFromCity(citiesSet, citiesIndex, citiesInfo, ccDict):
    """
    This infers the country for any given city, by looking into the adjacent dicts
    :param citiesSet: a set of city names
    :param citiesIndex:
    :param citiesInfo:
    :param ccDict: 
    :return: potential_countries : a set fo countries derives from the list of cities
    """
    potential_countries = set()
    for city in citiesSet:
        geonameidCity = citiesIndex[city.lower()][0]  # TODO: this is tricky, we might have more cities with same name
        country_code = citiesInfo[geonameidCity][4]
        potential_countries.add(ccDict[country_code])
    return potential_countries


def getUserLocation(locationField, citiesIndex, citiesInfo, countriesIndex, countriesInfo):
    """
    Takes in input the user_location field and tries various tokenizations to derive 
    potential cities and countries in the free text
    :param locationField: the user_location field 
    :param citiesIndex: 
    :param citiesInfo: 
    :param countriesIndex: 
    :param countriesInfo: 
    :return: cities, countries - 2 sets of potential cities and countries
    """

    potentialCities = set()
    potentialCountries = set()

    if (locationField == "") or (locationField is None):
        return potentialCities, potentialCountries

    # 1. split by / - the only char that is not in the tokenizer!
    if "/" in locationField:
        locArray = locationField.split("/")
        for token in locArray:
            city, country = getLocationsFromToken(token.strip().lower(), citiesIndex, citiesInfo, countriesIndex, countriesInfo)
            if city or country:
                potentialCities.add(city)
                potentialCountries.add(country)

    if "," in locationField:
        locArray = locationField.split(",")
        for token in locArray:
            city, country = getLocationsFromToken(token.strip().lower(), citiesIndex, citiesInfo, countriesIndex, countriesInfo)
            if city or country:
                potentialCities.add(city)
                potentialCountries.add(country)

    if len(potentialCities)==0 and len(potentialCountries)==0:
        # 2. tokenize with util and get unigrams, bigrams and trigrams - to lower
        # unigrams
        tokenList = twokenize.tokenize(locationField.lower())
        tokens = ngrams.window_no_twitter_elems(tokenList, 1)
        for token in tokens:
            city, country = getLocationsFromToken(token.strip(), citiesIndex, citiesInfo, countriesIndex, countriesInfo)
            if city or country:
                potentialCities.add(city)
                potentialCountries.add(country)

        # bigrams
        tokens = ngrams.window_no_twitter_elems(tokenList, 2)
        for token in tokens:
            city, country = getLocationsFromToken(token.strip(), citiesIndex, citiesInfo, countriesIndex, countriesInfo)
            if city or country:
                potentialCities.add(city)
                potentialCountries.add(country)

        # trigrams
        tokens = ngrams.window_no_twitter_elems(tokenList, 3)
        for token in tokens:
            city, country = getLocationsFromToken(token, citiesIndex, citiesInfo, countriesIndex, countriesInfo)
            if city or country:
                potentialCities.add(city)
                potentialCountries.add(country)

    cities, countries = cleanSets(potentialCities, potentialCountries)
    return cities, countries


def getFinalUserLocation(user_cities, user_countries, inferred_countries):
    """
    This decides upon the final city and country of a user.
    :param user_cities: 
    :param user_countries: 
    :param inferred_countries: 
    :return: 2 strings: city, country
    """
    city = None
    country = None

    if len(user_cities) == 1:
        city = next(iter(user_cities))

    if len(user_countries) == 1 and len(inferred_countries) == 1:
        if next(iter(user_countries))== next(iter(inferred_countries)):
            country = next(iter(user_countries))

    if len(user_countries) == 1 and len(inferred_countries) == 0:
        country = next(iter(user_countries))

    if len(user_cities) == 1 and len(user_countries) == 0 and len(inferred_countries) == 1:
        country = next(iter(inferred_countries))

    if len(user_countries) > 0 and len(inferred_countries) == 1:
        country = next(iter(inferred_countries))

    # this means we have a city and ambiguous country tagging,
    # but since we can't infer country we must dismiss city
    # if (city is not None) and (country is None):
    #     city = None
    # this also eliminates a lot of ok options
    return city, country


def hasGeoInformation(tweet):
    return tweet["coordinates"] is not None or tweet["place"] is not None


# def getUserLocationProfile(tweet):
#     return tweet['user']['location']


def getLocationData(tweet):
    """
    These can always have None values; e.g no coordinates, no city, no user location
    :param tweet:
    :return:
    """
    if tweet["coordinates"] is not None:
        tweet_coords = tweet['coordinates']['coordinates']  # returns a list [longitude, latitude]
    else:
        tweet_coords = None

    if tweet["place"] is not None:
        if tweet["place"]["place_type"] == "city":
            tweet_place_city = tweet["place"]["name"].lower()  # if place type == city
            tweet_place_country = tweet["place"]["country"].lower()
            tweet_place_country_code = tweet["place"]["country_code"]
        else:
            tweet_place_city = None
            tweet_place_country = tweet["place"]["country"].lower()
            tweet_place_country_code = tweet["place"]["country_code"]
    else:
        tweet_place_city = None
        tweet_place_country = None
        tweet_place_country_code = None

    user_location = tweet['user']['location']

    return tweet_coords, tweet_place_city, tweet_place_country, tweet_place_country_code, user_location


def inferCountryByGeolocation(tweet, countries_geojson):

    ### geo either the coordinates or the bb of the place
    geo_info_tweet = None
    if tweet["coordinates"] is not None:
        geo_info_tweet = shape(tweet["coordinates"])
    elif tweet["place"] is not None:
        geo_info_tweet = shape(tweet["place"]['bounding_box'])

    ### search which contry matches countries_geojson
    for feature in countries_geojson['features']:
        geo_country = shape(feature['geometry'])

        # returning the country that matches the intersection
        if geo_country.intersects(geo_info_tweet):
            return str(feature['properties']['name'].encode('utf-8')).lower()

    # returning None if there is no country intersecting the geo_info
    return None

