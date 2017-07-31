from elasticsearch import Elasticsearch
import json
import os
import sys
import datetime
import time
os.chdir("/home/vinicius/git/cnr/food101/")
# os.chdir("/home/foodmap/food101/")
sys.path.append(os.getcwd())
from elasticsearch import Elasticsearch, RequestError


# auxiliar functions
def get_datetime_date(date_int):
    str_date = str(date_int)
    return datetime.date(int(str_date[0:4]), int(str_date[4:6]), int(str_date[6:8]))


def get_datetime_month(date_int):
    str_date = str(date_int)
    return datetime.date(int(str_date[0:4]), int(str_date[4:6]), 1)


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

def compute_agg_index():
    numIndex = 1
    categories = get_category()
    max_result_window = 10000000
    es = get_es()

    for cat in categories:
        # replacing with underscoring
        cat = str.replace(cat, ' ', '_')

        # using the index trend
        results_agg = es.search(index='trend', doc_type='tweet', size=max_result_window, body={
            "size": max_result_window,
            "query": {
                "bool": {
                    "should": [
                        {"term": {"text_categories.keyword": str(cat)}},
                        {"term": {"img_categories.keyword": str(cat)}}
                    ]}
            },
            "aggs": {
                "agg_country": {
                    "terms": {
                        "field": "country.keyword",
                        "size": max_result_window
                    },
                    "aggs": {
                        "agg_date": {
                            "terms": {
                                #                    "field": "created_at_datetime",
                                "field": "created_at_day",
                                "size": max_result_window
                            }
                        }
                    }
                }
            }
        })

        # create the agg index by day
        for agg_country in results_agg['aggregations']['agg_country']['buckets']:
            country = agg_country['key']
            print cat, country, "count", len(agg_country['agg_date']['buckets']), "doc_error:", \
            results_agg['aggregations']['agg_country']['doc_count_error_upper_bound']
            for agg_date in agg_country['agg_date']['buckets']:
                date = agg_date['key']
                count = agg_date['doc_count']

                dic_cout = {
                    "category": cat
                    , "date": date
                    , "country": country
                    , "count": count
                    , "datetime_date": get_datetime_date(date)
                    #                 , "datetime_month": get_datetime_month(date)
                }

                es.index(index='agg', doc_type='count', id=numIndex, body=dic_cout)
                numIndex += 1
    # break
    print 'finished!'


def clean_agg_index():
    es = get_es()
    es.delete_by_query(index='agg', doc_type='count', body={
        'query': {
            "match_all" : {}
        }
    })

if __name__ == '__main__':
    while True:
        clean_agg_index()
        compute_agg_index()



