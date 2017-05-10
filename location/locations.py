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

            # first split into columns
            locationData = line.split("\t")
            geonameid = int(locationData[0])
            name = locationData[1].lower()
            asciiname = locationData[2]
            alternatenames = locationData[3]
            latitude = float(locationData[4])
            longitude = float(locationData[5])
            countrycode = locationData[8]
            population = int(locationData[14])
            timezone = locationData[17]

            # put names in the Index
            # usually one entry in the list, but when duplicates, we have more geonameid in the list
            if name not in stopwords:
                if ascii:
                    citiesIndex[asciiname.lower()].append(geonameid)
                else:
                    citiesIndex[name.lower()].append(geonameid)
            alt_names = alternatenames.split(",")
            for alt_name in alt_names:
                citiesIndex[alt_name.lower()].append(geonameid)

            # put city info in the Info dictionary
            if ascii:
                citiesInfo[geonameid] = tuple([name, asciiname, longitude, latitude, countrycode, population, timezone])
            else:
                citiesInfo[geonameid] = tuple([name, asciiname, longitude, latitude, countrycode, population, timezone])


        print "All cities with all name: ", len(citiesIndex)
        print "All cities unique geonameid:  ", len(citiesInfo)
        return citiesIndex, citiesInfo


class Countries:
    def __init__(self):
        pass

    @staticmethod
    def loadAlternateNames(geonameidList, countriesIndex, filename="./location/alternateNames.txt", dump=False):
        """
        This adds alternate names to countries and places them in the 
        :param geonameidList: the geonameids list of the countries in our dictionary; alternateName.txt file contains a
        lot of other alternate names, so we fil ter just the ones referring to countries
        :param countriesIndex: the alternateName to geonameid index , keeping al synonims but pointing to the same instance
        :param filename: which alernateNames file to lead; we have the initial one and a smaller version only for 
        countries named <alternateNamesSmall.txt>
        :param dump: if we should write to file a subsample of lines from filename
        :return: 
        """
        i=0
        if dump:
            outputWriter = codecs.open("./alternateNamesSmall.txt", "w", "utf-8")
        inpurReader = codecs.open(filename, "r", "utf-8")
        for line in inpurReader:
            i+=1
            lineData = line.split("\t")
            # print lineData
            # break
            geonameid = int(lineData[1])
            if geonameid in geonameidList:
                if dump:
                    outputWriter.write(line)
                countriesIndex[lineData[3].lower()] = geonameid
            if i % 1000000 == 0:
                print "Scanning file, line ", i
        if dump:
            outputWriter.close()
        return countriesIndex

    @staticmethod
    def countryCodeDict(countryDict):
        """
        Maps the country code to country name
        There are some duplicates for GB (UK) so we have less country codes in the initial country dictionary
        :param countryDict: 
        :return:
        """
        ccDict = dict()
        for k, v in countryDict.items():
            if len(v) != 5:
                print "Attention", k, v
            else:
                ccDict[v[4]] = v[0]
        print "Len of country code dict", len(ccDict)
        return ccDict

    @staticmethod
    def loadFromFile(filename="./location/countryInfo.txt"):
        """
        #ISO	ISO3	ISO-Numeric	fips	Country	Capital	Area(in sq km)	Population	Continent	tld	CurrencyCode
        CurrencyName	Phone	Postal Code Format	Postal Code Regex	Languages	geonameid	neighbours	EquivalentFipsCode
        :param filename:
        :return:
        """
        # print "current dir: ", os.getcwd()
        countriesIndex = defaultdict(list)
        countriesInfo = defaultdict(tuple)
        for line in codecs.open(filename, "r", "utf-8"):
            if not line.startswith("#") and line != "\n":
                # split the columns
                countryData = line.split("\t")
                name = countryData[4].lower()
                capital = countryData[5]
                population = countryData[7]
                continent = countryData[8]
                countryCode = countryData[0]
                geonameid = int(countryData[16])

                # put name in index
                if (name not in stopwords):
                    countriesIndex[name.lower()].append(geonameid)

                # put data in info dict
                if (name not in stopwords): # see if keeping this condition
                    countriesInfo[geonameid] = tuple([name, capital, population, continent, countryCode])

        # adding some synonims for UK
        countriesIndex["uk"].append(countriesIndex["united kingdom"])
        countriesIndex["england"].append(countriesIndex["united kingdom"])

        # extend with alternatenames
        countriesIndex = Countries.loadAlternateNames(countriesInfo.keys(), countriesIndex, filename="./alternateNamesSmall.txt", dump=False)

        print "All countries with all names: ", len(countriesIndex)
        print "All countries unique geonameid:  ", len(countriesInfo)
        return countriesIndex, countriesInfo


if __name__ == '__main__':

    # load cities and countries
    citiesIndex, citiesInfo = Cities.loadFromFile(filename="./cities15000.txt")
    countriesIndex, countriesInfo = Countries.loadFromFile(filename="./countryInfo.txt")

    # citiesAscii = locations.Cities.loadFromFile(ascii=True)
    ccDict = Countries.countryCodeDict(countriesInfo)
