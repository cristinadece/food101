import codecs
import logging
import os
from collections import defaultdict
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

stopwords = ["dalai", "buy", "best", "deal", "obama", "clinton", "police", "goes", "reading", "born", "manage", "gay",
             "barry", "dinar", "sale", "march", "nice", "mary", "vladimir", "zug", "boom", "anna", "gap", "york", "bar",
             "salt", "wedding", "of", "boston", "lincoln", "washington"]

stopwordsEuro = ["washington", "perth", "lincon", "roman"]

# eg New York
# [[[-24.08203125,14.0939571778],[-24.08203125,66.9988437919],[70.13671875,66.9988437919],[70.13671875,14.0939571778],
# [-24.08203125,14.0939571778]]]
# -24.08203125,14.0939571778,70.13671875,66.9988437919
# Europe Bounding Box:	-31.2660(v), 27.6363(e), 39.8693(s), 81.0088

eurasiaBB = [tuple([-24.08203125, 14.0939571778]), tuple([70.13671875, 66.9988437919])]
europeBB = [tuple([-24.08203125, 14.0939571778]), tuple([70.13671875, 66.9988437919])]

def inBB(lon, lat, boundingbox=eurasiaBB):
    lonMin = boundingbox[0][0]
    lonMax = boundingbox[1][0]
    latMin = boundingbox[0][1]
    latMax = boundingbox[1][1]
    return lonMin < lon < lonMax and latMin < lat < latMax

def loadUSstates(filename="resources/us_states.tsv"):
    us_states_list = list()
    for line in codecs.open(filename, "r", "utf-8"):
        state_data = line.split()
        if len(state_data) ==3:
            us_states_list.append(state_data[0].lower() + " " + state_data[1].lower())
            us_states_list.append(state_data[2].lower())
        else:
            us_states_list.append(state_data[0].lower())
            us_states_list.append(state_data[1].lower())
    us_states_list.append("usa")
    us_states_list.append("us")

    ### wtf
    us_states_list.remove("ok")
    us_states_list.remove("de")
    us_states_list.remove("la")
    us_states_list.remove("hi")
    us_states_list.remove("il")
    return us_states_list

class Cities:

    def __init__(self):
        pass

    @staticmethod
    def loadFromFile(filename="resources/cities15000.txt", ascii=False):
        """
        options: filename="resources/cities15000inBB.txt" or filename="resources/cities15000.txt"
        The BB is EURASIA

        This method load a dictionary of cities where the key is either the name or the asciiname
        Final version : for mentions: Africa, Asia,
        :param filename:
        :param ascii: True if we want the dictionary to have the asciinames as key, False otherwise
        :return:
        """
        citiesDict = defaultdict(tuple)
        for line in codecs.open(filename, "r", "utf-8"):
            locationData = line.split("\t")
            name = locationData[1].lower()
            asciiname = locationData[2]
            latitude = float(locationData[4])
            longitude = float(locationData[5])
            countrycode = locationData[8]
            population = int(locationData[14])
            timezone = locationData[17]
            continent = timezone.split("/")[0]
            if (name not in stopwords) and (population > 50000) and continent in ["Africa", "Asia", "Europe"]:
                if ascii:
                    citiesDict[asciiname.lower()] = tuple([name, asciiname, longitude, latitude, countrycode, population, timezone])
                else:
                    citiesDict[name.lower()] = tuple([name, asciiname, longitude, latitude, countrycode, population, timezone])
        print "All cities: ", len(citiesDict)
        return citiesDict


    @staticmethod
    def filterEuropeanCities(citiesDict):
        citiesEurope = defaultdict(tuple)

        for city, cityTuple in citiesDict.iteritems():
            # try:
            #     print cityTuple[6]
            # except:
            #     print city
            if ("Europe" in cityTuple[6]) and (city not in stopwordsEuro):
                citiesEurope[city] = cityTuple
        print "European cities: ", len(citiesEurope)
        return citiesEurope

    @staticmethod
    def filterCitiesInBB(filename):
        new_file = filename.replace(".txt", "") + "inBB.txt"
        output = codecs.open(new_file, "w", "utf-8")
        for line in codecs.open(filename, "r", "utf-8"):
            locationData = line.split("\t")
            latitude = float(locationData[4])
            longitude = float(locationData[5])
            if inBB(longitude, latitude, eurasiaBB):
                output.write(line)
        output.close()


class Countries:

    def __init__(self):
        pass

    @staticmethod
    def loadFromFile(filename="resources/countryInfo.txt"):
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
                if (name not in stopwords) and continent in ["EU", "AS", "AF"]:
                    countriesDict[name.lower()] = tuple([name, capital, population, continent, countryCode])
        countriesDict["uk"] = countriesDict["united kingdom"]
        countriesDict["england"] = countriesDict["united kingdom"]
        print "All countries: ", len(countriesDict)
        return countriesDict


    @staticmethod
    def filterEuropeanCountries(countriesDict, cities = None):
        """

        :param worldLocations:
        :return:
        """

        countriesEurope = defaultdict(tuple)
        for country, countryTuple in countriesDict.iteritems():
            if countryTuple[3] == "EU" and country != "jersey":
                countriesEurope[country] = countryTuple

        print "European countries: ", len(countriesEurope)
        return countriesEurope


    @staticmethod
    def countryCodeDict(countryDict):
        """
        Maps the country code to country name
        !!! Attention, we should do it for all Countries instead of just european
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


    @staticmethod
    def filterCountriesInBB(filename):
        """
        We can do this based on the capital coordinates to simplify stuff.
        For each country we have the capital and we search that capital in the Cities Dict, take the coords and if they
        are in the BB it means the country is in BB.
        :param filename:
        :return:
        """
        pass


if __name__ == '__main__':
    logger = logging.getLogger("locations.py")
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s;%(levelname)s;%(message)s")

    loadUSstates()

    # cities = Cities.loadFromFile()
    # citiesEU = Cities.filterEuropeanCities(cities,)
    # print len(citiesEU)
    # print citiesEU.keys()[:100]
    #
    # countries = Countries.loadFromFile()

