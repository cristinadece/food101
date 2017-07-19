import json
from flask import Flask, request
from flask_restful import Resource, Api
from es_trend_queries import get_categories_trends_filtered_by_country, get_countries_trends_filtered_by_category
from cartodb_trend_sync import sync_db_view
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)

class Status (Resource):
    def get(self):
        return {
            'name': 'Trends'
            , 'status': 'on'
        }

class CountriesTrends(Resource):

    def post(self):
        category = request.form['category']
        dateBegin = request.form['dateBegin']
        dateEnd = request.form['dateEnd']
        analysis_type = request.form['analysis_type']
        result = {"results": get_countries_trends_filtered_by_category(category, dateBegin, dateEnd, analysis_type)}
        result = json.dumps(result)
        return result

class CategoriesCountry(Resource):

    def post(self):
        country = request.form['country']
        dateBegin = request.form['dateBegin']
        dateEnd = request.form['dateEnd']
        analysis_type = request.form['analysis_type']
        result = {"results": get_categories_trends_filtered_by_country(country, dateBegin, dateEnd, analysis_type)}
        result = json.dumps(result)
        return result


class CartoDBTrends(Resource):

    def post(self):
        category = request.form['category']
        dateBegin = request.form['dateBegin']
        dateEnd = request.form['dateEnd']
        analysis_type = request.form['analysis_type']
        session = request.form['session']
        lst_country = get_countries_trends_filtered_by_category(category, dateBegin, dateEnd, analysis_type)
        sync_db_view(session, category, lst_country)
        return { "message": "ok" }


api.add_resource(Status, '/status')
api.add_resource(CountriesTrends, '/countriestrends')
api.add_resource(CategoriesCountry, '/categoriestrends')
api.add_resource(CartoDBTrends, '/cartodbview')

if __name__ == '__main__':
    print "Start Trend Api"
    app.run(host='0.0.0.0', port=5001, debug=True)
