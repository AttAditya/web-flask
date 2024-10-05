from flask import session, request, jsonify, send_file, redirect
from modules.extensions import f
from datetime import datetime, timezone
from uuid import uuid1
from io import BytesIO
from base64 import b64decode

def add_routes(app, dbs):
    content_db = dbs["content"]
    tags_db = dbs["tags"]
    content_dr = dbs["content_drive"]
    thumbnails_dr = dbs["thumbnails_drive"]
    accounts_db = dbs["accounts"]
    analytics_db = dbs["analytics"]

    def is_logged_in() -> bool:
        """
        Check if user is logged in...
        """

        if "userid" not in session: return False
        if not accounts_db.get(session.get("userid")): return False

        return True

    @app.route("/a/new")
    @app.route("/article/new")
    def article_new():
        if not is_logged_in(): return redirect("/user/in")
        
        user_data = accounts_db.get(session.get("userid"))
        if "create" not in user_data["permissions"]: return redirect("/404")
        
        return f("content/article/new.html")

    @app.route("/upload/article", methods=["POST"])
    def upload_article():
        article_data = request.get_json()
        aid = uuid1().hex

        content_dr.put(f"{aid}.html", article_data["content"].encode("utf-8"))
        if article_data["thumbnail"].startswith("data:"):
            image_data = b64decode(article_data["thumbnail"].replace("data:image/png;base64,", ""))
            thumbnails_dr.put(f"{aid}.png", image_data)
            article_data["thumbnail"] = f"/article/{aid}/thumbnail"

        content_db.put({
            "name": article_data["name"],
            "tags": article_data["tags"],
            "thumbnail": article_data["thumbnail"],
            "date": datetime.now(timezone.utc).strftime("%d %b %Y %I:%M:%S %p"),
            "authors": article_data["authors"]
        }, aid)

        for tag in article_data["tags"] + ["recents", "all"]:
            tag_data = tags_db.get(tag)
            if not tag_data: tag_data = {"articles": []}

            tag_data["articles"].insert(0, aid)

            if "headline" in tag and len(tag_data["articles"]) > 15: tag_data["articles"] = tag_data["articles"][:15]
            if tag == "recents" and len(tag_data["articles"]) > 25: tag_data["articles"] = tag_data["articles"][:25]

            tags_db.put(tag_data, tag)
        
        for author in article_data["authors"]:
            author_data = accounts_db.get(author)
            if not author_data: continue

            author_data["articles"].insert(0, aid)
            accounts_db.put(author_data, author)

        return jsonify({"status": "200", "msg": "OK", "id": aid})

    @app.route("/a/<article_id>/meta")
    @app.route("/article/<article_id>/meta")
    def article_meta(article_id: str):
        article_meta_data = content_db.get(article_id)
        if not article_meta_data: return jsonify({"status": "404", "msg": "Article not found"})

        article_meta_data.update({"status": "200", "msg": "OK", "id": article_id})

        if "key" in article_meta_data: del article_meta_data["key"]
        
        return jsonify(article_meta_data)

    @app.route("/a/<article_id>/content")
    @app.route("/article/<article_id>/content")
    def article_content(article_id: str):
        content_file = content_dr.get(f"{article_id}.html")
        
        if not content_file: return "Not Found"
        content_stream = content_file.read()
        content_data = content_stream.decode()
        
        return content_data

    @app.route("/a/<article_id>/thumbnail")
    @app.route("/article/<article_id>/thumbnail")
    def article_thumbnail(article_id: str):
        thumbnail_file = thumbnails_dr.get(f"{article_id}.png")
        
        if not thumbnail_file: return "Not Found"
        thumbnail_stream = thumbnail_file.read()

        return send_file(BytesIO(thumbnail_stream), download_name=f"{article_id}-thumbnail.png", mimetype="image/png")

    @app.route("/a/<article_id>")
    @app.route("/article/<article_id>")
    def article_page(article_id: str):
        article_meta_data = content_db.get(article_id)
        if not article_meta_data: return redirect("/404")

        analytics_data = analytics_db.get(article_id)
        if not analytics_data: analytics_data = {"views": 0}
        analytics_data["views"] += 1
        analytics_db.put(analytics_data, article_id)
        
        if "key" in article_meta_data: del article_meta_data["key"]
        
        article_meta_data["id"] = article_id

        return f("content/article/page.html", **article_meta_data)

    @app.route("/a/<article_id>/analytics")
    @app.route("/article/<article_id>/analytics")
    def article_analytics(article_id: str):
        article_meta_data = analytics_db.get(article_id)
        if not article_meta_data: return redirect("/404")

        return jsonify(article_meta_data)

    @app.route("/a/<article_id>/edit")
    @app.route("/article/<article_id>/edit")
    def article_edit(article_id: str):
        if not is_logged_in(): return redirect("/user/in")

        article_data = content_db.get(article_id)

        if not article_data: return redirect("/404")
        if session["userid"] not in article_data["authors"]:
            if "edit" not in accounts_db.get(session["userid"])["permissions"]:
                return redirect("/404")
        
        article_data["id"] = article_id
        article_data["tagstr"] = ",".join(article_data["tags"])
        article_data["authorsstr"] = ",".join(article_data["authors"])
        article_data["content"] = article_content(article_id)
        if "key" in article_data: del article_data["key"]

        return f("content/article/edit.html", **article_data)

    @app.route("/update/article", methods=["POST"])
    def update_article():
        article_data = request.get_json()
        aid = article_data["id"]

        article_delete(aid)

        content_dr.put(f"{aid}.html", article_data["content"].encode("utf-8"))
        if article_data["thumbnail"].startswith("data:"):
            image_data = b64decode(article_data["thumbnail"].replace("data:image/png;base64,", ""))
            thumbnails_dr.put(f"{aid}.png", image_data)
            article_data["thumbnail"] = f"/article/{aid}/thumbnail"

        content_db.put({
            "name": article_data["name"],
            "tags": article_data["tags"],
            "thumbnail": article_data["thumbnail"],
            "date": datetime.now(timezone.utc).strftime("%d %b %Y %I:%M:%S %p"),
            "authors": article_data["authors"]
        }, aid)

        for tag in article_data["tags"] + ["recents", "all"]:
            tag_data = tags_db.get(tag)
            if not tag_data: tag_data = {"articles": []}

            tag_data["articles"].insert(0, aid)

            if "headline" in tag and len(tag_data["articles"]) > 15: tag_data["articles"] = tag_data["articles"][:15]
            if tag == "recents" and len(tag_data["articles"]) > 25: tag_data["articles"] = tag_data["articles"][:25]

            tags_db.put(tag_data, tag)
        
        for author in article_data["authors"]:
            author_data = accounts_db.get(author)
            if not author_data: continue

            author_data["articles"].insert(0, aid)
            accounts_db.put(author_data, author)

        return jsonify({"status": "200", "msg": "OK", "id": aid})

    @app.route("/a/<article_id>/delete")
    @app.route("/article/<article_id>/delete")
    def article_delete(article_id: str):
        if not is_logged_in(): return redirect("/user/in")

        article_data = content_db.get(article_id)

        if not article_data: return redirect("/404")
        if session["userid"] not in article_data["authors"]:
            if "delete" not in accounts_db.get(session["userid"])["permissions"]:
                return redirect("/404")

        for tag in article_data["tags"] + ["recents", "all"]:
            tag_data = tags_db.get(tag)
            
            if not tag_data: continue
            if article_id not in tag_data["articles"]: continue

            del tag_data["articles"][tag_data["articles"].index(article_id)]
            
            if not tag_data["articles"]:
                tags_db.delete(tag)
                continue
            
            tags_db.put(tag_data, tag)
        
        for author in article_data["authors"]:
            if not author: continue
            author_data = accounts_db.get(author)
            
            if not author_data: continue
            if article_id not in author_data["articles"]: continue

            del author_data["articles"][author_data["articles"].index(article_id)]
            accounts_db.put(author_data, author)
        
        content_db.delete(article_id)
        content_dr.delete(f"{article_id}.html")

        if analytics_db.get(article_id): analytics_db.delete(article_id)

        return "Article Deleted"
    
    @app.route("/articles/meta", methods=["POST"])
    def articles_meta():
        requested_topics = request.get_json()
        data = {}

        for topic, quantity in requested_topics.items():
            topic_articles = tags_db.get(topic)

            if not topic_articles: topic_articles = {"articles": []}

            articles_meta = []
            start = 0
            amount = 0

            if isinstance(quantity, list):
                start = quantity[0]
                amount = quantity[1]
            else:
                amount = quantity
            
            articles_id = topic_articles["articles"][start:start+amount]

            for article_id in articles_id:
                article_content = content_db.get(article_id)

                if "key" in article_content: del article_content["key"]
                
                article_content["id"] = article_id

                articles_meta.append(article_content)

            data.update({topic: articles_meta})

        return jsonify({**data, "status": 200, "msg": "OK"})

