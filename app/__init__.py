import logging
from flask import Flask, request, redirect, jsonify, send_from_directory
from flask_restful import Resource, Api
from flask_cors import CORS
from config import Config, basedir
import pymongo


client = pymongo.MongoClient(Config.MONGODB_URI)
db = client[Config.MONGODB_DB]

def custom_static(filename):
    print('static', filename)
    return send_from_directory(f'{basedir}/static/images', filename)


def create_app():
    app = Flask(__name__, static_folder='../static')
    app.add_url_rule('/api/v1/static/images/<path:filename>', 'custom_static', custom_static)
    cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
    api = Api(app, prefix='/api/v1')
    from app.main import rest_resources


    api.add_resource(rest_resources.Text2Image, '/generate-image', '/generate-image/<id>')
    api.add_resource(rest_resources.GenerateDescription, '/generate-description', '/generate-description/<id>')
    api.add_resource(rest_resources.GenerateText, '/summarize-text', '/summarize-text/<id>')

    return app
