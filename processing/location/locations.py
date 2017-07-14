import codecs
import json
from shapely.geometry import mapping, shape
from collections import defaultdict


# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

stopwords = ["dalai", "buy", "best", "deal", "obama", "clinton", "police", "goes", "reading", "born", "manage", "gay",
             "barry", "dinar", "sale", "march", "nice", "mary", "vladimir", "zug", "boom", "anna", "gap", "york", "bar",
             "salt", "wedding", "of", "lincoln", "wa", "san", "jersey", "allen", "florida", "santa cruz", "springs",
             "bay", "island", "sur"]
"""
http://download.geonames.org/export/dump/
"""

class Cities:
    """
    Cities loads all the cities in the cities15000.txt files, meaning cities with a population bigger than 15000.
    An issue here is that there are a lot of homonymes in lots of countries, so we need a list of tuples for every name.
    City_name -> [list of tulpes to cities in different countries, with the same name]
    """
    def __init__(self):
        pass


    @staticmethod
    def loadFromFile(filename="./resources/cities15000.txt", ascii=False, withSynonym=False):
        """
        This method load a dictionary of cities where the key is either the name or the asciiname.
        
        :param filename: a table with city information from geonames dump:  cities15000.txt.
        :param ascii: True if we want the dictionary to have the asciinames as key, False otherwise.
        :param withSynonym: This also loads the synonyms for city names and adds them to the first dictionary citiesIndex
        
        :return: 2 dictionaries: citiesIndex, citiesInfo
            - citiesIndex: a dictionary of lists, usually the length of a list is 1, but when the name of a city appears 
            in different countries, then the list is bigger than 1. e.g Paris, France vs. Paris, Texas, USA.
                k: name or alternatename
                v: list of geonameid - the biggest city is the first element of the list
            - citiesInfo: a simple dictionary
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
            asciiname = locationData[2].lower()
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
                    cityName = asciiname
                else:
                    cityName = name

                if len(citiesIndex[cityName]) != 0:
                    # put biggest city first in the list
                    existentCityGeonameid = citiesIndex[cityName][0]
                    existentCityPopulation = citiesInfo[existentCityGeonameid][5]
                    if population>existentCityPopulation:
                        citiesIndex[cityName].insert(0,geonameid)
                    else:
                        citiesIndex[cityName].append(geonameid)
                else: # means first entry
                    citiesIndex[cityName].append(geonameid)

            # adding syns
            citiesIndex["new york"].extend(citiesIndex["new york city"])
            citiesIndex["nyc"].extend(citiesIndex["new york city"])
            citiesIndex["roma"].extend(citiesIndex["rome"])
            citiesIndex["milano"].extend(citiesIndex["milan"])
            if withSynonym: #todo: this makes it so that the duplicates have same name and are in the list of geonameid
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
    def loadAlternateNames(geonameidList, countriesIndex, filename="./resources/alternateNamesSmall.txt"):
        """
        This adds alternate names to countries and places them in the 
        :param geonameidList: the geonameids list of the countries in our dictionary; alternateName.txt file contains a
        lot of other alternate names, so we filter just the ones referring to countries
        
        :param countriesIndex: the alternateName to geonameid index , keeping al synonims but pointing to the same instance
        :param filename: a smaller version only for countries named <alternateNamesSmall.txt>
        
        :return: the countryIndex passed as argument enriched with new country alternate names
        """
        i=0
        inpurReader = codecs.open(filename, "r", "utf-8")
        for line in inpurReader:
            i+=1
            lineData = line.split("\t")
            geonameid = int(lineData[1])
            if geonameid in geonameidList:
                countriesIndex[lineData[3].lower()].append(geonameid)
            if i % 1000000 == 0:
                print "Scanning file, line ", i
        return countriesIndex


    @staticmethod
    def countryCodeDict(countriesInfo):
        """
        Maps the country code to country name
        There are some duplicates for GB (UK) so we have less country codes in the initial country dictionary
        
        :param countriesInfo: a dictionary with geonameid and info tuple about a country
        
        :return: a dictionary of country code pointing to country name 
        """
        ccDict = dict()
        for k, v in countriesInfo.items():
            if len(v) != 5:
                print "Attention", k, v
            else:
                ccDict[v[4]] = v[0]
        ccDict["JE"] = "jersey"
        print "Len of country code dict", len(ccDict)
        return ccDict


    @staticmethod
    def loadFromFile(filename="./resources/countryInfo.txt", withSynonym=True):
        """
        #ISO	ISO3	ISO-Numeric	fips	Country	Capital	Area(in sq km)	Population	Continent	tld	CurrencyCode
        CurrencyName	Phone	Postal Code Format	Postal Code Regex	Languages	geonameid	neighbours	EquivalentFipsCode
        
        :param filename: usually countryInfo.txt resource file with all countries in the world
        :param withSynonym: specifies whether to load alternate names for countries or just keep the official name
        
        :return: 2 dictionaries: countriesIndex, countriesInfo
            - countriesIndex: a dictionary of lists, usually the length of a list is 1
                k: name or alternatename
                v: list of geonameid
            - countriesInfo: a simple dictionary
                k: geonameid
                v: tuple with info
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

        # adding some synonyms for UK
        countriesIndex["uk"].extend(countriesIndex["united kingdom"])
        countriesIndex["england"].extend(countriesIndex["united kingdom"])

        # extend with alternatenames
        if withSynonym:
            countriesIndex = Countries.loadAlternateNames(countriesInfo.keys(), countriesIndex, filename="./resources/alternateNamesSmall.txt")

        print "All countries with all names: ", len(countriesIndex)
        print "All countries unique geonameid:  ", len(countriesInfo)
        return countriesIndex, countriesInfo

    @staticmethod
    def loadGeoJsonCountries(filename="./resources/geoshapes/world_borders.geojson"):
        # check also with countries.geo.json
        geojs_countries = []
        with open(filename, 'r') as f:
            geojs_countries = json.load(f)
        return geojs_countries

if __name__ == '__main__':

    # load cities and countries
    citiesIndex, citiesInfo = Cities.loadFromFile(filename="./processing/resources/cities15000.txt")
    countriesIndex, countriesInfo = Countries.loadFromFile(filename="./processing/resources/countryInfo.txt")

    # citiesAscii = locations.Cities.loadFromFile(ascii=True)
    ccDict = Countries.countryCodeDict(countriesInfo)
