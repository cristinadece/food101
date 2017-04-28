import codecs
import os
from collections import defaultdict
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

stopwords = ["dalai", "buy", "best", "deal", "obama", "clinton", "police", "goes", "reading", "born", "manage", "gay",
             "barry", "dinar", "sale", "march", "nice", "mary", "vladimir", "zug", "boom", "anna", "gap", "york", "bar",
             "salt", "wedding", "of", "lincoln", "wa"]


class Cities:
    """
    Cities loads all the cities in the cities15000.txt files, meaning cities with a population bigger than 15000.
    An issue here is that there are a lot of homonymes in lots of countries, so we need a list of tuples for every name.
    City_name -> [list of tulpes to cities in different countries, with the same name]
    """
    def __init__(self):
        pass

    @staticmethod
    def loadFromFile(filename="./location/cities15000.txt", ascii=False):
        """
        This method load a dictionary of cities where the key is either the name or the asciiname.
        
        :param filename: a table with city information from geonames dump:  cities15000.txt.
        :param ascii: True if we want the dictionary to have the asciinames as key, False otherwise.
        
        :return: 2 dictionaries:
            - a dictionary of lists, usually the length of a list is 1, but when the name of a city appears 
        in different countries, then the list is bigger than 1. e.g Paris, France vs. Paris, Texas, USA.
                k: name or alternatename
                v: list of geonameid 
            - a simple dictionary
                k: geonameid
                v: tuple with info
        """
        citiesIndex = defaultdict(list)
        citiesInfo = defaultdict(tuple)
        for line in codecs.open(filename, "r", "utf-8"):
            locationData = line.split("\t")
            name = locationData[1].lower()
            asciiname = locationData[2]
            alternatenames = locationData[3]  ## this is a list or string?
            latitude = float(locationData[4])
            longitude = float(locationData[5])
            countrycode = locationData[8]
            population = int(locationData[14])
            timezone = locationData[17]
            #if (name not in stopwords) and (population > 50000):
            #todo : the key may repeat itself!!!! we need to fix this with another key!!!
            if name not in stopwords:
                if ascii:
                    citiesDict[asciiname.lower()].append(tuple([name, asciiname, longitude, latitude, countrycode, population, timezone]))
                else:
                    citiesDict[name.lower()].append(tuple([name, asciiname, longitude, latitude, countrycode, population, timezone]))
        print "All cities: ", len(citiesDict)
        return citiesDict


class Countries:
    def __init__(self):
        pass

    def findAlternateNames(self):
        pass

    @staticmethod
    def loadFromFile(filename="./location/countryInfo.txt"):
        """
        #ISO	ISO3	ISO-Numeric	fips	Country	Capital	Area(in sq km)	Population	Continent	tld	CurrencyCode
        CurrencyName	Phone	Postal Code Format	Postal Code Regex	Languages	geonameid	neighbours	EquivalentFipsCode
        :param filename:
        :return:
        """
        print "current dir: ", os.getcwd()
        countriesDict = defaultdict(tuple)
        print filename
        for line in codecs.open(filename, "r", "utf-8"):
            if not line.startswith("#") and line != "\n":
                countryData = line.split("\t")
                name = countryData[4].lower()
                capital = countryData[5]
                population = countryData[7]
                continent = countryData[8]
                countryCode = countryData[0]
                if (name not in stopwords):
                    countriesDict[name.lower()] = tuple([name, capital, population, continent, countryCode])
        countriesDict["uk"] = countriesDict["united kingdom"]
        countriesDict["england"] = countriesDict["united kingdom"]
        print "All countries: ", len(countriesDict)
        return countriesDict


    @staticmethod
    def countryCodeDict(countryDict):
        """
        Maps the country code to country name
        :param countryDict:
        :return:
        """
        ccDict = dict()
        for k, v in countryDict.items():
            if len(v) != 5:
                print "Attention", k, v
            else:
                ccDict[v[4]] = v[0]
        return ccDict


if __name__ == '__main__':

    # load cities and countries
    # countries = locations.Countries.loadFromFile()
    cities = Cities.loadFromFile(filename="./cities15000.txt")
    # citiesAscii = locations.Cities.loadFromFile(ascii=True)
    # ccDict = locations.Countries.countryCodeDict(countries)
