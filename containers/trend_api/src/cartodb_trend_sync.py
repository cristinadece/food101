from itertools import groupby
from carto.auth import APIKeyAuthClient
from carto.sql import SQLClient
from carto.exceptions import CartoException


def get_auth():
    USERNAME="hpclab"
    APIKEY = "e97d6bbf73f61f1faa5a3bafb81c370bdc131de5"
    USR_BASE_URL = "https://{user}.carto.com/".format(user=USERNAME)
    return APIKeyAuthClient(api_key=APIKEY, base_url=USR_BASE_URL)

def sync_db_view(session, category, analysis_type, interval, lst_coutry):
    # session = 'fixed'
    auth_client = get_auth()
    sql = SQLClient(auth_client)

    if session is not None:
        sql_str = "delete from trend_value where session = '{session}';".format(session=session)
        sql.send(sql_str)
    else:
        sql_str = "delete from trend_value where category = '{category}' and analysis_type = '{analysis_type}' and interval = '{interval}' ;".format(category=category, analysis_type=analysis_type, interval=interval)
        sql.send(sql_str)

    for country_cur in lst_coutry:
        try:
            country_cur['country'] = country_cur['country'].replace('\'',' ')

            if isinstance(country_cur['value'], float):
                country_cur['value'] = round(country_cur['value'], 4)

            insert_value = "'{country}', {value}, '{session}', '{category}', '{analysis_type}', '{interval}'".format(country=country_cur['country'], value=country_cur['value'], category=category, session=session,  analysis_type= analysis_type, interval=interval)
            sql_str = "insert into trend_value (country, value, session, category,  analysis_type, interval) values ({insert_value});".format(insert_value=insert_value)
            sql.send(sql_str)
        except Exception as e:
            print "some error ocurred", e, sql_str