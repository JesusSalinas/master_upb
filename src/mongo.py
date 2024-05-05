
import os
import json

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
    
    #To-do delete this method
    def get_collection(self, collection):
        try:
            self.collection = self.db[collection]
            print('COLLECTION FETCH SUCCESSFULL!')
        except Exception as e:
            print('COLLECTION FETCH FAILED!', e)

    def insert_document(self, document, collection):
        try: 
            result = self.db[collection].insert_one(document)
            print('INSERTED DOCUMENT SUCCESSFULL! - ID:', result.inserted_id)
        except Exception as e:
            print('INSERTED DOCUMENT FAILED!', e)

    def update_document(self, filter, collection, new_value):
        try: 
            result = self.db[collection].update_one(filter, {"$set": new_value})
            if result.modified_count > 0:
                print('UPDATED DOCUMENT SUCCESSFULL!')
            else:
                print('DOCUMENT NOT FOUND!')
                
        except Exception as e:
            print('UPDATED DOCUMENT FAILED!', e)
    
    def fetch_documents(self, collection):
        if collection in self.db.list_collection_names():
            coll = self.db[collection]
            if coll.count_documents({}) > 0:
                documents = self.db[collection].find()
                print('FETCHED DOCUMENTS SUCCESSFULL!')
                documents_list = []
                for doc in documents:
                    documents_list.append(json.dumps(doc, default=str, indent=4))
                return documents_list
            else: 
                print('DOCUMENTS NOT FOUND!')
                return False
        else:
            print('COLLECTION NOT FOUND!')
            return False
        
    def find_document(self, collection, query):
        if collection in self.db.list_collection_names():
            coll = self.db[collection]
            document = coll.find_one(query)
            if document != None:
                print('FETCHED DOCUMENT SUCCESSFULL!')
                document_json = json.dumps(document, default=str, indent=4)
                return document_json
            else: 
                print('DOCUMENT NOT FOUND!')
                return False
        else:
            print('COLLECTION NOT FOUND!')
            return False

