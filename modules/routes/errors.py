from flask import request, jsonify
from datetime import datetime

def add_routes(app, dbs):
    errors_db = dbs["errors"]
    
    @app.errorhandler(404)
    @app.route("/404")
    def err404(*_, **__):
        return jsonify(["404 - Page Not Found"])

    @app.route("/errors/post", methods=["POST"])
    def errors_post():
        data = request.get_json()
        errors_db.put({"data": data}, datetime.now().strftime("%d %b %Y %I:%M:%S %p"))

        return ""

    @app.route("/errors/get")
    def errors_get():
        res = errors_db.fetch()
        all_items = res.items
        while res.last:
            res = errors_db.fetch(last=res.last)
            all_items += res.items

        return "\n<br>\n".join(list(map(str, sorted(res.items, reverse=True))))
