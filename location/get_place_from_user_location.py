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

    if citiesIndex[token]:
        geonamesidCity = citiesIndex[token]
        city = citiesInfo[geonamesidCity][0]
    if countriesIndex[token]:
        geonamesidCountry = countriesIndex[token]
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
        geonameidCity = citiesIndex[city.lower()]
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


if __name__ == '__main__':

    pass
    # load cities and countries
    citiesIndex, citiesInfo = Cities.loadFromFile()
    countriesIndex, countriesInfo = Countries.loadFromFile()

    # citiesAscii = locations.Cities.loadFromFile(ascii=True)
    ccDict = Countries.countryCodeDict(countriesInfo)
