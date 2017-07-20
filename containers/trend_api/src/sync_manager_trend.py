from cartodb_trend_sync import sync_db_view
from es_trend_queries import get_countries_trends_filtered_by_category
import time
import datetime



def getCategories():
    htCategoryList = list()
    with open("../../../resources/categories.txt") as g:
        for line in g:
            ht = line.lower().replace("\r\n", "").replace(" ", "_")
            htCategoryList.append(ht)

    return htCategoryList


if __name__ == '__main__':
    print "Sync Trend Manager Started", datetime.datetime.now()
    time_sync = 60 * 60 * 12  # in seconds
    dateBegin = 0
    dateEnd = 20201231

    analysis_types = ['frequency', 'trend', 'popularity']
    categories = getCategories()

    # the main thread in loop
    while True:
        session = None
        for category in categories:
            print 'sync category:', category
            for analysis_type in analysis_types:
                lst_country = get_countries_trends_filtered_by_category(category, dateBegin, dateEnd, analysis_type)
                sync_db_view(session, category, analysis_type, lst_country)
        print 'finished syncing going to sleep', datetime.datetime.now()
        time.sleep(time_sync)