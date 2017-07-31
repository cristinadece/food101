from elasticsearch import Elasticsearch
from collections import defaultdict
import numpy as np
from scipy import stats
import datetime
from collections import Counter

def get_es():
    es_url = 'test.tripbuilder.isti.cnr.it'
    es_port = 9200
    return Elasticsearch([es_url], http_auth=('elastic', 'changeme'), port=es_port)


def datetimetotimestamp(dt):
    return (dt - datetime(1970, 1, 1)).total_seconds()


def split_intervat_in_buckets(interval, daily_frequencies):
    last_ts = datetimetotimestamp(
        datetime.strptime(str(max(tpl[0] for tpl in daily_frequencies)),
                          '%Y%m%d'))

    tsinterval = interval * 3600 * 24
    interval_dict = Counter()
    for x, freq in daily_frequencies:
        ts = datetimetotimestamp(datetime.strptime(str(x), '%Y%m%d'))
        tsid = int((ts - last_ts) / tsinterval)
        interval_dict[tsid] += freq

    minkey = min(interval_dict.keys())
    return sorted([(tsid - minkey, freq) for tsid, freq in interval_dict.iteritems()])


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


def get_total_freq_country(country, dateBegin, dateEnd):
    """
    Given a country, it sums up all frequencies for all food categories in a
    time interval.
    :param country:
    :return:
    """
    result_country = query_filter_by_country(country, dateBegin, dateEnd)
    total = 0
    for x in result_country['hits']['hits']:
        total += x["_source"]['count']
    return total

def get_total_freq_category(category, dateBegin, dateEnd):
    """
    Given a category, it sums up all frequencies for all the countries in a time
    interval
    :param category:
    :return:
    """
    result_categ = query_filter_by_category(category, dateBegin, dateEnd)
    total = 0
    for x in result_categ['hits']['hits']:
        total += x["_source"]['count']
    return total

def get_countries_trends_filtered_by_category(category, dateBegin, dateEnd, analysis_type="trend", interval=None):
    # tweets of that category
    if interval == 1:
        interval = None

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
        elif analysis_type == "relative_frequency":
            total_sum = get_total_freq_country(country, dateBegin, dateEnd)
            country_trend[country] = sum([y for x, y in sorted_counts]) / (1.0 * total_sum)
        elif analysis_type == "popularity":
            if interval is None:
                y = [y for x, y in sorted_counts]
            else:
                new_intervals = split_intervat_in_buckets(interval,
                                                          sorted_counts)
                y = [y for x, y in new_intervals]
            country_trend[country] = stats.zscore(y)[-1]
        elif analysis_type == "trend":
            if interval is None:
                y = [y for x, y in sorted_counts]
            else:
                new_intervals = split_intervat_in_buckets(interval,
                                                          sorted_counts)
                y = [y for x, y in new_intervals]
            x = np.arange(len(y))
            try:
                regression = np.polyfit(x, y, 1)
                country_trend[country] = regression[0]
            except:
                # the for doesn't work for this example:
                # np.polyfit(np.array([0]), np.array([1]), 1)
                # some versions of numpy return nan, as should we
                country_trend[country] = np.nan


    # build the dic as json and also filter nan values
    country_trend = [{'country': x, 'value': y} for x,y in country_trend.iteritems() if y is not None and not np.isnan(y)]

    # order the values
    country_trend.sort(key=lambda item: item['value'], reverse=True)
    return country_trend

def get_categories_trends_filtered_by_country(country, dateBegin, dateEnd, analysis_type="trend", interval=None):

    if interval == 1:
        interval = None

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
        if analysis_type == "frequency":
            category_trend[category] = sum([y for x, y in sorted_counts])
        elif analysis_type == "relative_frequency":
            total_sum = get_total_freq_category(category, dateBegin, dateEnd)
            category_trend[category] = sum([y for x, y in sorted_counts]) / (1.0 * total_sum)
        elif analysis_type == "popularity":
            if interval is None:
                y = [y for x, y in sorted_counts]
            else:
                new_intervals = split_intervat_in_buckets(interval,
                                                          sorted_counts)
                y = [y for x, y in new_intervals]
            category_trend[category] = stats.zscore(y)[-1]
        elif analysis_type == "trend":
            if interval is None:
                y = [y for x, y in sorted_counts]
            else:
                new_intervals = split_intervat_in_buckets(interval,
                                                          sorted_counts)
                y = [y for x, y in new_intervals]
            x = np.arange(len(y))
            try:
                regression = np.polyfit(x, y, 1)
                category_trend[category] = regression[0]
            except:
                # the for doesn't work for this example:
                # np.polyfit(np.array([0]), np.array([1]), 1)
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