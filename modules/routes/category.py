from flask import jsonify
from modules.extensions import f

def add_routes(app, dbs):
    tags_db = dbs["tags"]

    @app.route("/c/<category>")
    @app.route("/category/<category>")
    def category_page(category: str):
        return f("content/tags/category.html", name=category)

    @app.route("/c/<category>/get")
    @app.route("/category/<category>/get")
    def category_get(category: str):
        res = tags_db.fetch()
        all_items = res.items
        while res.last:
            res = tags_db.fetch(last=res.last)
            all_items += res.items
        
        all_tags_data = res.items
        all_tags_data.sort(key=lambda x: len(x["articles"]), reverse=True)
        
        tags = [{
            "name": tag["key"],
            "length": len(tag["articles"])
        } for tag in all_tags_data if category in tag["key"]]

        return jsonify(tags)
