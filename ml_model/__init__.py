from abc import ABC, abstractmethod
import os
import logging
from config import Config
from dotenv import load_dotenv
import pymongo

from config import basedir

path = os.path.join(basedir, '.env')
load_dotenv(path)
upload_path = os.path.join(basedir, 'static/descriptions_images/')

client = pymongo.MongoClient(Config.MONGODB_URI)
db = client[Config.MONGODB_DB]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TaskModel(ABC):
    def __init__(self, message_data):
        self.message_data = message_data
    
    @abstractmethod
    def run(self):
        pass
