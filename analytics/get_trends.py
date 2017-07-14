"""
Tools for trend/popularity analysis.

"""
from collections import defaultdict
import numpy as np
from elasticsearch import Elasticsearch
from scipy import stats

es = Elasticsearch(['foodmap.isti.cnr.it'], http_auth=('elastic', 'changeme'), port=9200)

# Query by food category - Fig. 2b,c Map/Report of Trends/Popularity
def query_by_category(category, dateBegin, dateEnd):
    """
    It queries the ES Trend index
    :param category: str
        101 food categories
    :param dateBegin: int
        e.g 20170405
    :param dateEnd: int
        e.g 20170408
    :return:
        : dict
        An Elastic search response as a dictionary
    """
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


# Query by food category - Fig. 2a Report of Trends/Popularity
def query_by_country(country, dateBegin, dateEnd):
    """
    It queries the ES Trend index
    :param country: str
        any of the countries in the dictionary, little more than 250
    :param dateBegin: int
        e.g 20170405
    :param dateEnd: int
        e.g 20170408
    :return:
        : dict
        An Elastic search response as a dictionary
    """
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


def get_trend_per_country(query_result, analysis_type="trend"):
    """
    Given the result of the query_by_category, we get all the countries and the daily counts in order to compute
    trend and popularity.

    Given a food category we compute trends/popularity for all countries in a given time interval.

    :param query_result: dict
        An ES result dictionary from the agg index
    :param analysis_type: string
        Either "trend" or "popularity"  or "frequency".
        - The trend method computes the derivative of a simple linear
        regression bet fitting the distribution of counts per day.
        https://docs.scipy.org/doc/numpy-1.3.x/reference/generated/numpy.polyfit.html
        - The popularity score computes the zscore for the last day in the interval (dateEnd). Calculates the z score
        of each value in the sample, relative to the sample mean and standard deviation.
        https://docs.scipy.org/doc/scipy-0.19.0/reference/generated/scipy.stats.zscore.html
        - The frequency sums up all the daily values in the time interval
    :return:
        : dict
        A dictionary of <country, derivative/zscore > give as input a certain food category
    """
    # result = query_by_category(category)

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
                # the for doesn't work for this example: np.polyfit(np.array([0]), np.array([1]), 1)
                # some versions of numpy return nan, as should we
                country_trend[country] = np.nan

    return country_trend


def get_trend_per_category(query_result, analysis_type="trend"):
    """
    Given the result of the query_by_country, we get all the categories and the daily counts in order to compute
    trend and popularity.

    Given a country we compute trends/popularity for all food categories in a given time interval.

    :param query_result: dict
        An ES result dictionary from the agg index.
    :param analysis_type: string
        Either "trend" or "popularity" or "frequency".
        - The trend method computes the derivative of a simple linear
        regression bet fitting the distribution of counts per day.
        https://docs.scipy.org/doc/numpy-1.3.x/reference/generated/numpy.polyfit.html
        - The popularity score computes the zscore for the last day in the interval (dateEnd). Calculates the z score
        of each value in the sample, relative to the sample mean and standard deviation.
        https://docs.scipy.org/doc/scipy-0.19.0/reference/generated/scipy.stats.zscore.html
        - The frequency sums up all the daily values in the time interval
    :return:
        : dict
        A dictionary of <category, derivative/zscore > give as input a certain country
    """

    # result = query_by_country(country)

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
        elif analysis_type == "popularity":
            category_trend[category] = stats.zscore([y for x, y in sorted_counts])[-1]
        elif analysis_type == "trend":
            y = [y for x, y in sorted_counts]
            x = np.arange(len(y))
            try:
                regression = np.polyfit(x, y, 1)
                category_trend[category] = regression[0]
            except:
                # the for doesn't work for this example: np.polyfit(np.array([0]), np.array([1]), 1)
                # some versions of numpy return nan, as should we
                category_trend[category] = np.nan

    return category_trend
