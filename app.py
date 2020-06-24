from flask import Flask, jsonify
from flask_restful import Resource, Api
import requests, json, anilist, yify
from flask import Response, render_template

app = Flask(__name__)
api = Api(app)

class AnimeINFO(Resource):
	def get(self, query):
		return jsonify(anilist.search_anilist(query, type='ANIME'))

class MangaINFO(Resource):
	def get(self, query):
		return jsonify(anilist.search_anilist(query, type='MANGA'))

class Yify(Resource):
	def get(self, query):
		return jsonify(yify.search_yify(query))

class Home(Resource):
	def get(self):
		resources = {
			"AnimeINFO": {
				"parameter": '/animeinfo/<query>',
				"example": '/animeinfo/overlord',
				"help": 'performs a search using the provided query and returns up to 10 results fetched from AniList.'
			}, 
			"MangaINFO": {
				"parameter": '/mangainfo/<query>',
				"example": '/mangainfo/overlord',
				"help": 'performs a search using the provided query and returns up to 10 results fetched from AniList.'
			}
		}
		return resources


#################################################
api.add_resource(Home, '/')
api.add_resource(Yify, '/yify/<query>')
api.add_resource(AnimeINFO, '/animeinfo/<query>')
api.add_resource(MangaINFO, '/mangainfo/<query>')
if __name__ == '__main__':
	app.run(port=80)
