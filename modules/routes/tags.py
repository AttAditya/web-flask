from flask import request, jsonify
from modules.extensions import f

def add_routes(app, dbs):
    tags_db = dbs["tags"]
    
    @app.route("/t/<tag>")
    @app.route("/tag/<tag>")
    @app.route("/tagged/<tag>")
    def tag_page(tag: str):
        return f("content/tags/tagged.html", name=tag)

    @app.route("/t/<tag>/get")
    @app.route("/tag/<tag>/get")
    @app.route("/tagged/<tag>/get")
    def tag_get(tag: str):
        results = tags_db.get(tag)
        return f("content/tags/category.html", name=tag)

    @app.route("/articles/get", methods=["POST"])
    def articles_get():
        requested_topics = request.get_json()
        data = {}

        for topic, quantity in requested_topics.items():
            topic_articles = tags_db.get(topic)
            if not topic_articles: topic_articles = {"articles": []}
            if isinstance(quantity, list):
                data.update({topic: topic_articles["articles"][quantity[1] - 1:quantity[0] + quantity[1]]})
                continue

            data.update({topic: topic_articles["articles"][:quantity]})

        return jsonify({**data, "status": 200, "msg": "OK"})
