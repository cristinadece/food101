import requests
from elasticsearch import Elasticsearch
from collections import defaultdict
import numpy as np
from scipy import stats


def get_es():
    es_url = 'test.tripbuilder.isti.cnr.it'
    es_port = 9200
    return Elasticsearch([es_url], http_auth=('elastic', 'changeme'), port=es_port)


def query_filter_by_category(category, dateBegin, dateEnd):
    es = get_es()
    result = es.search(index='agg', doc_type='count', size=100000, body={
        "query": {
            "bool": {
                "filter": [
                    {"term": {"category.keyword": category}},
                    {"range": {
                        "date": {
                            "gte": dateBegin,
                            "lte": dateEnd
                        }
                    }}
                ]
            }
        }
    })
    return result


def query_filter_by_country(country, dateBegin, dateEnd):
    es = get_es()
    result = es.search(index='agg', doc_type='count', size=100000, body={
        "query": {
            "bool": {
                "filter": [
                    {"term": {"country.keyword": country}},
                    {"range": {
                        "date": {
                            "gte": dateBegin,
                            "lte": dateEnd
                        }
                    }}
                ]
            }
        }
    })
    return result


def get_countries_trends_filtered_by_category(category, dateBegin, dateEnd, analysis_type="trend"):
    # tweets of that category
    query_result = query_filter_by_category(category, dateBegin, dateEnd)

    country_dict = defaultdict(list)
    for x in query_result['hits']['hits']:
        country_dict[x["_source"]['country']].append(tuple((x["_source"]['date'], x["_source"]['count'])))

    country_trend = defaultdict(float)
    for country, values in country_dict.iteritems():
        # sort list by date ascending
        sorted_counts = sorted(values, key=lambda x: x[0])
        # we refer to the current day in the interval
        if analysis_type == "frequency":
            country_trend[country] = sum([y for x, y in sorted_counts])
        elif analysis_type == "popularity":
            country_trend[country] = stats.zscore([y for x, y in sorted_counts])[-1]
        elif analysis_type == "trend":
            y = [y for x, y in sorted_counts]
            x = np.arange(len(y))
            try:
                regression = np.polyfit(x, y, 1)
                country_trend[country] = regression[0]
            except:
                # the fir doesn't work for this example: np.polyfit(np.array([0]), np.array([1]), 1)
                # some versions of numpy return nan, as should we
                country_trend[country] = np.nan


    # build the dic as json and also filter nan values
    country_trend = [{'country': x, 'value': y} for x,y in country_trend.iteritems() if y is not None and not np.isnan(y)]

    # order the values
    country_trend.sort(key=lambda item: item['value'], reverse=True)
    return country_trend


def get_categories_trends_filtered_by_country(country, dateBegin, dateEnd, analysis_type="trend"):
    # tweets of that country
    query_result = query_filter_by_country(country, dateBegin, dateEnd)

    category_dict = defaultdict(list)
    for x in query_result['hits']['hits']:
        category_dict[x["_source"]['category']].append(tuple((x["_source"]['date'], x["_source"]['count'])))

    category_trend = defaultdict(float)
    for category, values in category_dict.iteritems():
        # sort list by date ascending
        sorted_counts = sorted(values, key=lambda x: x[0])
        # we refer to the current day in the interval
        if analysis_type == "popularity":
            category_trend[category] = stats.zscore([y for x, y in sorted_counts])[-1]
        elif analysis_type == "trend":
            y = [y for x, y in sorted_counts]
            x = np.arange(len(y))
            try:
                regression = np.polyfit(x, y, 1)
                category_trend[category] = regression[0]
            except:
                # the fir doesn't work for this example: np.polyfit(np.array([0]), np.array([1]), 1)
                # some versions of numpy return nan, as should we
                category_trend[category] = np.nan



    # build the dic for the json and also filter nan values
    category_trend = [{'category': x, 'value': y} for x, y in category_trend.iteritems() if
             y is not None and not np.isnan(y)]

    # order the values
    category_trend.sort(key=lambda item: item['value'], reverse=True)
    return category_trend

    category_trend = [(x, y) for x, y in category_trend.iteritems()]
    return category_trend