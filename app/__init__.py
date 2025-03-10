import logging
from flask import Flask, request, redirect, jsonify, send_from_directory
from flask_restful import Resource, Api
from flask_cors import CORS
from config import Config, basedir
import pymongo
import os
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

client = pymongo.MongoClient(Config.MONGODB_DATABASE_URL)
logger.info(f"{os.environ.get('MONGODB_DATABASE_URL')=}")
logger.info(f"{Config.MONGODB_DATABASE_URL=}")
logger.info(f"Connected to MongoDB: {client}")
# db = client[Config.MONGODB_DB]
db = client[Config.MONGODB_DATABASE_NAME]
logger.info(f"Database: {db}")

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
