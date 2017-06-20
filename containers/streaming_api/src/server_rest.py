from flask import Flask, request
from flask_restful import Resource, Api
# from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
# CORS(app)

from elasticsearch import Elasticsearch

class Status (Resource):
    def get(self):
        return {
            'name': 'Sync'
            , 'status': 'on'
        }

class Sync (Resource):
    def get(self):
        es = Elasticsearch(['test.tripbuilder.isti.cnr.it'], http_auth=('elastic', 'changeme'), port=9200)
        res = es.search(index="stream", doc_type='tweet_snippet', size=100, body={"query": {"match_all": {}}})
        return [x['_source'] for x in res['hits']['hits']]


api.add_resource(Status, '/status')
api.add_resource(Sync, '/sync')

if __name__ == '__main__':
    print "Start Sync Api"
    app.run(host='0.0.0.0', port=5000, debug=True)
