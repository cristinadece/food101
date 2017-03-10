#!/usr/bin/env python
'''
StreamBBTwitter : MyStreamer
@euthor: Cristina Muntean (cristina.muntean@isti.cnr.it)
@date: 9/22/16
-----------------------------
 or here: http://www.kalisch.biz/2013/10/harvesting-twitter-with-python/

'''

import json
import os
from datetime import date

import uuid as uuid
from twython import TwythonStreamer

currentDate = date.today()
DUMP_DIR = '/data/tweets/food-tweets'

#check if file exists
file_name = DUMP_DIR + "/food-tweets-" + str(currentDate) + ".json"

if os.path.isfile(file_name):
    uuid = str(uuid.uuid1())
    new_file_name = DUMP_DIR + "/food-tweets-" + str(currentDate) + "-" + uuid + ".json"
    currentFile = open(new_file_name, "w")
else:
    currentFile = open(file_name, "w")


class MyStreamer(TwythonStreamer):

    def on_success(self, data):
        global currentDate, currentFile


        if self.is_current_date():
            currentFile.write(json.dumps(data)+'\n')
        else:
            currentFile.close()
            currentDate = date.today()
            currentFile = open(DUMP_DIR + "/food-tweets-" + str(currentDate) + ".json", "w")
            currentFile.write(json.dumps(data)+'\n')

    def on_error(self, status_code, data):
        print status_code

    @staticmethod
    def is_current_date():
        return date.today() == currentDate

