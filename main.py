from __future__ import annotations
from os import environ

import logging
from flask import Flask

logging.getLogger("werkzeug").setLevel(logging.ERROR)

app = Flask("TWTDB", static_folder="res", static_url_path="/res")
app.secret_key = environ.get("SECRET", "default")

from modules.database import databases
from modules.routes import add_routes

add_routes(app, databases)

if __name__ == "__main__":
	app.run("0.0.0.0", 8000)

