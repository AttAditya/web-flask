from pymongo import MongoClient
try:
    from keys import SECRETS
except ImportError:
    from os import environ
    SECRETS = {
        "MONGO": environ["MONGO"]
    }

mongo_client = MongoClient(SECRETS["MONGO"])
mongo_db = mongo_client["WTN"]
