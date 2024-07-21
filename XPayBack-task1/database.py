from pymongo import MongoClient
import gridfs
import psycopg2

# PostgreSQL Database Setup
POSTGRESQL_DATABASE_URL = "postgres://<UserName>:<Password>@<Host>:<Port>/<DatabaseName>?sslmode=require"

# MongoDB Database Setup
MONGO_CONNECTION_STRING = "mongodb+srv://<username>:<password>@cluster0.aov6zre.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
mongo_client = MongoClient(MONGO_CONNECTION_STRING)
mongo_db = mongo_client['XPayBackDB']
fs = gridfs.GridFS(mongo_db)
profile_collection = mongo_db['Profile']

# Ensure 'email' is indexed and unique in MongoDB
profile_collection.create_index('email', unique=True)

def get_postgresql_connection():
    conn = psycopg2.connect(POSTGRESQL_DATABASE_URL)
    return conn