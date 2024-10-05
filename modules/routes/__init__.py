from modules.extensions import f
from . import (
    errors,
    images,
    misc,
    user,
    articles,
    category,
    tags
)

def add_routes(app, dbs):
    modules = [
        errors,
        images,
        misc,
        user,
        articles,
        category,
        tags
    ]

    for module in modules:
        module.add_routes(app, dbs)
    
    @app.route("/")
    def home():
        return f("index.html")

