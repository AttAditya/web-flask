from pymongo import MongoClient
from keys import SECRETS

mongo_client = MongoClient(SECRETS["MONGO"])
mongo_db = mongo_client["WTN"]
