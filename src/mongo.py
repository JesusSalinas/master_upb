
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus

import os
from dotenv import load_dotenv
load_dotenv()

password = quote_plus(os.getenv('MONGO_PASS'))
user = quote_plus(os.getenv('MONGO_USER'))
db = os.getenv('MONGO_DB')
collection = os.getenv('MONGO_COLLECTION')

uri = 'mongodb+srv://' + user+ ':' + password + '@jesuscluster.hl2zshw.mongodb.net/?retryWrites=true&w=majority&appName=JesusCluster'

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client[db]

co = db[collection]

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

documentos = co.find()

print("Documentos en la colección:")
for documento in documentos:
    print(documento)


# Cerrar la conexión
client.close()