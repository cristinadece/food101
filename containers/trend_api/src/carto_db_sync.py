from itertools import groupby
from carto.auth import APIKeyAuthClient
from carto.sql import SQLClient
from carto.exceptions import CartoException


USERNAME="hpclab"
APIKEY = "e97d6bbf73f61f1faa5a3bafb81c370bdc131de5"
USR_BASE_URL = "https://{user}.carto.com/".format(user=USERNAME)
auth_client = APIKeyAuthClient(api_key=APIKEY, base_url=USR_BASE_URL)

def sync_db_view(category, lst_coutry):
    section = 'fixed'
    sql = SQLClient(auth_client)
    sql_str = "delete from trend_value where section = '{section}';".format(section=section)
    sql.send(sql_str)

    for country_cur in lst_coutry:
        try:
            insert_value = "'{country}', {value}, '{section}'".format(country=country_cur['country'], value=country_cur['value'], section=section)
            sql_str = "insert into trend_value (country, value, section) values ({insert_value});".format(insert_value=insert_value)
            sql.send(sql_str)
        except Exception as e:
            print "some error ocurred", e, sql_str