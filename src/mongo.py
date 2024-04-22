
import os

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
from dotenv import load_dotenv
load_dotenv()

env_password = quote_plus(os.getenv('DB_MONGO_PASS'))
env_user = quote_plus(os.getenv('DB_MONGO_USER'))
env_db = os.getenv('DB_MONGO_DB')
env_host = os.getenv('DB_MONGO_HOST')
env_uri = 'mongodb+srv://' + env_user+ ':' + env_password + '@' + env_host + '/'

class MongoDBConnector:
    def __init__(self):
        self.host = env_host
        self.username = env_user
        self.password = env_password
        self.database_name = env_db
        self.db = None
        self.client = None
        self.collection = None
    
    def connect(self):
        try:
            self.client = MongoClient(env_uri, server_api=ServerApi('1'))
            self.db = self.client[self.database_name]
            print('DB CONNECTION SUCCESSFULL!:', self.database_name)
        except Exception as e:
            print("DB CONNECTION FAILED!:", e)
    
    def disconnect(self):
        try:
            self.client.close()
            print('DB DISCONNECTION SUCCESSFULL!')
        except Exception as e:
            print('DB DISCONNECTION FAILED!:', e)
    
    def get_collection(self, collection_name):
        try:
            self.collection = self.db[collection_name]
            print('COLLECTION FETCH SUCCESSFULL!')
        except Exception as e:
            print('COLLECTION FETCH FAILED!', e)

    def insert_document(self, document):
        try: 
            result = self.collection.insert_one(document)
            print('INSERTED DOCUMENT SUCCESSFULL! - ID:', result.inserted_id)
        except Exception as e:
            print('INSERTED DOCUMENT FAILED!', e)
