from pandas import json

__author__ = 'cris'



class User:

    def __init__(self, id):
        self.id = id
        self.type = ""
        self.screen_name = ""
        self.location = ""
        self.tweet_locations = []
        self.tweet_coordinates = []



    def toString(self):
        return u"{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n".format(self.id, self.type, self.screen_name, self.location, self.tweet_locations, self.tweet_coordinates)


    def toJson(self):
        """

        :rtype : str
        """
        return json.dumps(self.__dict__)

    def setUserAttributes(self, type, location, screenname):
        self.type = type
        self.screen_name = screenname
        if location is not None:
            self.location = location



    def setTweetRelatedUserAttributes(self, place, coord):
        if place is not None:
            self.tweet_locations.append(place)
        if coord is not None:
            self.tweet_coordinates.append(coord)


    # ["216905308",{"id":"216905308","screen_name":"AishathShakeela","tweet_coordinates":[],"type":"NEUTRAL"}]
    # pickle
    @staticmethod
    def parseStringToUser(dict):
        pass