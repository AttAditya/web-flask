from os import environ

SECRETS = {
    "MONGO": environ.get("MONGO", "mongodb://localhost:27017")
}

