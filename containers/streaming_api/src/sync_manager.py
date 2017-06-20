import requests
import json
from elasticsearch import Elasticsearch
import time


es_url = 'test.tripbuilder.isti.cnr.it'
es_port = 9200
sync_cycle = 10

# update file
def sync_file():
    # query es for retrieval of the tweets
    es = Elasticsearch([es_url], http_auth=('elastic', 'changeme'), port=es_port)
    res = es.search(index="stream", doc_type='tweet_snippet', size=1000, body={"query": {"match_all": {}}})

    # cleaning results
    res_parsed = [x['_source'] for x in res['hits']['hits']]

    # dump as json and save in disk
    json_data = json.dumps(res_parsed)
    with open('stream.json', 'w') as outfile:
        json.dump(json_data, outfile)
        print 'file saved'

# push data into cartodb
def sync_cartodb():
    # url = 'https://www.googleapis.com/qpxExpress/v1/trips/search?key=mykeyhere'
    # payload = json.load(open("request.json"))
    # headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    # r = requests.post(url, data=json.dumps(payload), headers=headers)
    return 0

if __name__ == '__main__':
    print "Sync Manager Started"

    # the main thread in loop
    while True:
        sync_file()
        sync_cartodb()
        time.sleep(sync_cycle)







