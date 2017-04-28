"""

"""
# food101 : get_place_from_user_location
# Created by muntean on 4/26/17
import os
import sys

from location import locations
from tokenizer import twokenize, ngrams


def getLocationsFromToken(token, cityDict, countryDict):
    city = ""
    country = ""
    if cityDict[token]:
        city = token
    if countryDict[token]:
        # country = token
        country = countryDict[token][0]  # we take the name of the country from the tuple, elim. both UK and United K.
    return city, country


def cleanLists(potentialCities, potentialCountries):
    if "" in potentialCities:
        potentialCities.remove("")
    if "" in potentialCountries:
        potentialCountries.remove("")
    return potentialCities, potentialCountries


def inferCountryFromCity(citiesList, cityDict, ccDict):
    """
    This should be done by country code crossing
    :param citiesList: 
    :param cityDict: 
    :param ccDict: 
    :return: 
    """

    potential_countries = set()
    for city in citiesList:
        country_code = cityDict[city][4]
        potential_countries.add(ccDict[country_code])

    return potential_countries


def getUserLocation(locationField, cityDict, countryDict):
    """
    THis field is an empty string
    :param tweet:
    :return:
    """

    potentialCities = set()
    potentialCountries = set()

    # 1. split by / - the only char that is not in the tokeniker!
    if "/" in locationField:
        locArray = locationField.split("/")
        for token in locArray:
            city, country = getLocationsFromToken(token.strip().lower(), cityDict, countryDict)
            if city or country:
                potentialCities.add(city)
                potentialCountries.add(country)

    if "," in locationField:
        locArray = locationField.split(",")
        for token in locArray:
            city, country = getLocationsFromToken(token.strip().lower(), cityDict, countryDict)
            if city or country:
                potentialCities.add(city)
                potentialCountries.add(country)

    # 2. tokenize with util and get unigrams, bigrams and trigrams - to lower
    # unigrams
    tokenList = twokenize.tokenize(locationField.lower())
    tokens = ngrams.window_no_twitter_elems(tokenList, 1)
    for token in tokens:
        city, country = getLocationsFromToken(token.strip(), cityDict, countryDict)
        if city or country:
            potentialCities.add(city)
            potentialCountries.add(country)

    # bigrams
    tokens = ngrams.window_no_twitter_elems(tokenList, 2)
    for token in tokens:
        city, country = getLocationsFromToken(token.strip(), cityDict, countryDict)
        if city or country:
            potentialCities.add(city)
            potentialCountries.add(country)

    # trigrams
    tokens = ngrams.window_no_twitter_elems(tokenList, 3)
    for token in tokens:
        city, country = getLocationsFromToken(token, cityDict, countryDict)
        if city or country:
            potentialCities.add(city)
            potentialCountries.add(country)

    cities, countries = cleanLists(potentialCities, potentialCountries)
    return cities, countries


if __name__ == '__main__':

    pass
    # load cities and countries
    # countries = locations.Countries.loadFromFile()
    # cities = locations.Cities.loadFromFile()
    # citiesAscii = locations.Cities.loadFromFile(ascii=True)
    # ccDict = locations.Countries.countryCodeDict(countries)
