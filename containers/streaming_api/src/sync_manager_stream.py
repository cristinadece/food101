import requests
from carto.auth import APIKeyAuthClient
from carto.sql import SQLClient
from carto.exceptions import CartoException
from elasticsearch import Elasticsearch
import time
import datetime
import random
import json


def get_auth_carto():
    USERNAME="hpclab"
    APIKEY = "e97d6bbf73f61f1faa5a3bafb81c370bdc131de5"
    USR_BASE_URL = "https://{user}.carto.com/".format(user=USERNAME)
    return APIKeyAuthClient(api_key=APIKEY, base_url=USR_BASE_URL)


def get_es():
    es_url = 'localhost'
    es_port = 8055
    return Elasticsearch([es_url], http_auth=('elastic', 'changeme'), port=es_port)


# get the centroid of a bb
def point_centroid(points):
    x_coords = [p[0] for p in points]
    y_coords = [p[1] for p in points]
    _len = len(points)
    centroid_x = sum(x_coords)/_len
    centroid_y = sum(y_coords)/_len
    return [centroid_x, centroid_y]


def point_close_to_center(points):
    random_point_bb = random.choice(points)
    centroid = point_centroid(points)
    w_deviation = random.uniform(0, 0.25)
    point_x = centroid[0] + w_deviation * (random_point_bb[0] - centroid[0])
    point_y = centroid[1] + w_deviation * (random_point_bb[1] - centroid[1])
    return [point_x, point_y]

# push data into cartodb
def sync_carto_stream(first_sync, last_datetime):

    auth_client = get_auth_carto()
    es = get_es()

    # query last day
    query = {
        "query": {
            "range": {
                "created_at_datetime": {
                    "gte": "now-24h"
                }
            }
        },
        "sort": {
            "created_at_datetime": {"order": "desc"}
        }
    }

    # executing the query
    response = es.search(index="stream", doc_type='tweet', size=10000, body=query)

    # cleaning results
    tweets = [x['_source'] for x in response['hits']['hits']]

    # cleaning the tweet
    for i in range(0, len(tweets)):
        try:
            cur_tweet = tweets[i]
            cur_tweet['text'] = cur_tweet['text'].encode('utf-8')
            cur_tweet['text'] = cur_tweet['text'].replace('\'', ' ')
            cur_tweet['has_img'] = True if cur_tweet['media_url'] is not None else False
            cur_tweet['media_url'] = cur_tweet['media_url'] if cur_tweet['media_url'] is not None else 'http://cofunction.com/fp-images/NoImage/img_not_available.png'
            txt_cat = cur_tweet['text_categories']
            img_cat = cur_tweet['img_categories']

            cur_tweet['text_categories'] = ','.join(
                map(lambda x: x.encode('utf-8'), txt_cat)) if txt_cat is not None else ''

            # concating the results
            # cur_tweet['img_categories'] = ' - '.join(
            #     map(lambda x: 'label: {0}, score: {1}'.format(x['label'].encode('utf-8'), x['score']),
            #         img_cat)) if img_cat is not None and len(img_cat) > 0 else ''

            # taking only the first result
            if img_cat is not None and len(img_cat) > 0:
                if img_cat[0]['score'] < 7.0:
                    cur_tweet['result_classification'] = 'low confidence'
                elif img_cat[0]['score'] >= 10.0:
                    cur_tweet['result_classification'] = 'high confidence'
                else:
                    cur_tweet['result_classification'] = 'medium confidence'
                cur_tweet['img_categories'] = 'label: {0}, score: {1}'.format(img_cat[0]['label'], img_cat[0]['score'])
                # print img_cat[0]['label'], img_cat[0]['score'], cur_tweet['result_classification']
            else:
                cur_tweet['result_classification'] = 'text'

            cur_tweet['categories'] = cur_tweet['img_categories'] if img_cat is not None and len(img_cat) > 0 else cur_tweet['text_categories']
        except Exception as e:
            tweets.pop(i)
            print "error sync", e

    # sql client instance
    sql = SQLClient(auth_client)

    # delete the old tweets
    if first_sync:
        sql_str = sql_str = "delete from tweets_stream"
    else:
        sql_str = sql_str = "delete from tweets_stream where datetime < now() - interval '24 hour'"
    sql.send(sql_str)
    sql_str = ''

    # insert the last new data
    insert_count = 0
    update_last_datetime = None
    print 'inserting data...'
    for tweet in tweets:
        try:

            format_datetime = "%b %d %Y %H:%M:%S"

            coordinates = tweet['coords'] if tweet['coords'] is not None else point_close_to_center(
                tweet['bounding_box']['coordinates'][0])
            the_geom = "ST_GeomFromText('POINT({lng} {lat})', 4326)".format(lng=coordinates[0], lat=coordinates[1])

            insert_value = "{the_geom}, '{username}', '{img_category}', '{text_categories}', '{categories}', '{text}', {id}, '{media_url}', '{datetime}', '{datetime_formated}', {has_img}, '{result_classification}'".format(
                the_geom=the_geom, username=tweet['username'], img_category=str(tweet['img_categories']),
                text_categories=str(tweet['text_categories']), categories=str(tweet['categories']), text=tweet['text'], id=tweet['id'],
                media_url=tweet['media_url'], datetime=tweet['created_at_datetime'], datetime_formated=tweet['created_at_datetime'].replace('T', ' '), has_img=tweet['has_img'], result_classification=tweet['result_classification'])

            sql_insert = "insert into tweets_stream (the_geom, username, img_category, text_categories, categories, text, id, media_url, datetime, datetime_formated, has_img, result_classification) values ({insert_value});".format(
                insert_value=insert_value)

            # if syncing at the first time insert all the date
            if first_sync or last_datetime < tweet['created_at_datetime']:
                # insert tweet stream
                sql.send(sql_insert)
                insert_count = insert_count + 1

            # check compered to the last datime sync
            if last_datetime is None or last_datetime < tweet['created_at_datetime']:
                # is it higher than the number that should be
                if update_last_datetime is None:
                    update_last_datetime = tweet['created_at_datetime']
                elif update_last_datetime < tweet['created_at_datetime']:
                    update_last_datetime = tweet['created_at_datetime']

        except CartoException as e:
            print "some error ocurred", e, sql_insert
        except Exception as eg:
            print "some error ocurred", eg

    print 'finished sync. inserted: ', insert_count
    first_sync = False

    # update last datetime
    if update_last_datetime is not None:
        last_datetime = update_last_datetime

    return first_sync, last_datetime




### main method
if __name__ == '__main__':
    print "Sync Streamming Manager Started"
    time_sync = 30      # in seconds
    first_sync = True
    last_datetime = None

    # the main thread in loop
    while True:
        try:
            first_sync, last_datetime = sync_carto_stream(first_sync, last_datetime)
            print 'sleep', time_sync, "seconds", datetime.datetime.now()
        except Exception as e:
            print 'error', e
        finally:
            time.sleep(time_sync)
