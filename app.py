from flask import Flask, jsonify
from flask_restful import Resource, Api
import requests, json, anilist
from flask import Response, render_template


app = Flask(__name__)
api = Api(app)

class AnimeINFO(Resource):
	def get(self, query):
		return jsonify(anilist.search_anilist(query))



api.add_resource(AnimeINFO, '/anisearch/<query>')
if __name__ == '__main__':
	app.run(port=80)
