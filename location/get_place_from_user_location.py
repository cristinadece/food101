"""

"""
# food101 : get_place_from_user_location
# Created by muntean on 4/26/17
import os
import sys

from location import locations
from location.locations import Cities, Countries
from tokenizer import twokenize, ngrams


def getLocationsFromToken(token, citiesIndex, citiesInfo, countriesIndex, countriesInfo):
    """
    
    :param token: 
    :param citiesIndex: 
    :param citiesInfo: 
    :param countriesIndex: 
    :param countriesInfo: 
    :return: 
    """
    city = ""
    country = ""

    if citiesIndex[token] and len(citiesIndex[token])==1: #TODO: this condition is because we have more cities with same name
        geonamesidCity = citiesIndex[token][0]
        city = citiesInfo[geonamesidCity][0]
    if countriesIndex[token]:
        geonamesidCountry = countriesIndex[token][0]
        country = countriesInfo[geonamesidCountry][0]  # we take the name of the country from the tuple, elim. both UK and United K.
    return city, country


def cleanLists(potentialCities, potentialCountries):
    if "" in potentialCities:
        potentialCities.remove("")
    if "" in potentialCountries:
        potentialCountries.remove("")
    return potentialCities, potentialCountries


def inferCountryFromCity(citiesList, citiesIndex, citiesInfo, ccDict):
    """
    This should be done by country code crossing
    :param citiesList: 
    :param cityDict: 
    :param ccDict: 
    :return: 
    """

    potential_countries = set()
    for city in citiesList:
        geonameidCity = citiesIndex[city.lower()][0]  # TODO: this is tricky, we might have more cities with same name
        country_code = citiesInfo[geonameidCity][4]
        potential_countries.add(ccDict[country_code])
    return potential_countries


def getUserLocation(locationField, citiesIndex, citiesInfo, countriesIndex, countriesInfo):
    """
    THis field is an empty string
    :param tweet:
    :return:
    """

    potentialCities = set()
    potentialCountries = set()

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

    if len(potentialCities)==0 and potentialCountries==0:
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

    cities, countries = cleanLists(potentialCities, potentialCountries)
    return cities, countries


def getFinalUserLocation(user_cities, user_countries, inferred_countries):
    city = ""
    country = ""

    if len(user_cities) == 1:
        city = next(iter(user_cities))

    if len(user_countries) == 1 and len(inferred_countries) == 1:
        if next(iter(user_countries))== next(iter(inferred_countries)):
            country = next(iter(user_countries))

    if len(user_countries) == 1 and len(inferred_countries) == 0:
        country = next(iter(user_countries))

    if len(user_countries) == 0 and len(inferred_countries) == 1:
        country = next(iter(inferred_countries))

    # this means we have a city and ambiguous country tagging,
    # but since we can't infer country we must dismiss city
    if len(city) > 0 and len(country) == 0:
        city = ""

    return city, country



if __name__ == '__main__':

    pass
    # load cities and countries
    citiesIndex, citiesInfo = Cities.loadFromFile()
    countriesIndex, countriesInfo = Countries.loadFromFile()

    # citiesAscii = locations.Cities.loadFromFile(ascii=True)
    ccDict = Countries.countryCodeDict(countriesInfo)
