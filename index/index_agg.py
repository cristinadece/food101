from elasticsearch import Elasticsearch
import json
import os
import sys
import time
os.chdir("/home/foodmap/food101/")
sys.path.append(os.getcwd())
from elasticsearch import Elasticsearch, RequestError


def get_es():
    es = Elasticsearch(['foodmap.isti.cnr.it'], http_auth=('elastic', 'changeme'), port=9200)
    return es


def get_category():
    dir_file = os.path.join(os.getcwd(), "resources/categories.txt")
    categories = []

    with open(dir_file, 'r') as f:
        content = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
        categories = [str.lower(x.strip()) for x in content]
    print "total categories", len(categories)

def clean_agg_index():
    es = get_es()
    es.delete_by_query(index='agg', doc_type='count', body={
        'query': {
            "match_all" : {}
        }
    })




