# http://api.nal.usda.gov/ndb/reports/?ndbno=01009&type=b&format=json&api_key=twNtcNSu4kf27gWr464iyWp33XJ59wA8JXPivzYE

import requests
import json
import ast
import time

lst_id = []
lst_api_key = ["twNtcNSu4kf27gWr464iyWp33XJ59wA8JXPivzYE",  # vinicezarml@gmail.com
            "JnPFPBtJQmH8vbl9F6ibxym1XLvEkfAfL2pw0EHT", # chiara.renso@isti.cnr.it
            "ivK2ae81d9E7JfYISsJTxqTCBcNQvaVdTVwJTE8U", # rensochiara@gmail.com
            "eaJeZ0CH6gR7GoxTnKvVDqY2Qjhz0dRExJa4TrUW", # viniciuscezarml@gmail.com
            "GfW1x8VGMm0cdjdptGpJPEnWCTMjG112HhHampyL" # "vinicius.monteirodelira@isti.cnr.it"
            ]

# control variable
idx_api = 0
count_by_key = 0
count_general = 0
max_call_by_key = 950
sleep_time = 60 # in minutes

# load ids
with open('ids.txt', 'r') as f:
    for line in f:
        id_dic = ast.literal_eval(line)
        lst_id.append(id_dic["id"])

# dowload food
for id in lst_id:
    r = requests.get(
        "http://api.nal.usda.gov/ndb/reports/?ndbno=%s&type=b&format=json&api_key=%s" % (id, lst_api_key[idx_api])
    )
    # r.status_code

    food_json = r.json()
    count_by_key = count_by_key + 1
    count_general = count_general + 1

    if count_general % 100 == 0:
        print "total downloaded", count_general, "total by key", count_by_key

    if count_by_key % max_call_by_key == 0:
        # switch the api key
        print 'switch the api key'
        idx_api = idx_api + 1
        count_by_key = 1

        # sleep the crawler
        if idx_api % len(lst_api_key) == 0 and idx_api > 0:
            print 'sleep crawler'
            time.sleep(sleep_time*60)  # delays for 1 hour
            idx_api = 0


    with open('food_json.json', 'a') as f:
        json.dump(food_json, f)
        f.write('\n')

    with open("lastid_api.txt", "wb") as f:
        f.write(id)



