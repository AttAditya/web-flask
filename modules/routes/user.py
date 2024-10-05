from flask import session, request, jsonify, redirect
from modules.extensions import f, encrypt

def add_routes(app, dbs):
    accounts_db = dbs["accounts"]
    content_db = dbs["content"]

    def is_logged_in() -> bool:
        """
        Check if user is logged in...
        """

        if "userid" not in session: return False
        if not accounts_db.get(session.get("userid")): return False

        return True

    @app.route("/u/in")
    @app.route("/user/in")
    def user_sign_in():
        if is_logged_in(): return redirect("/dash")
        return f("/user/login/in.html")

    @app.route("/u/new")
    @app.route("/user/new")
    def user_sign_up():
        if is_logged_in(): return redirect("/dash")
        return f("/user/login/new.html")

    @app.route("/u/out")
    @app.route("/user/out")
    def user_sign_out():
        session.clear()
        return redirect("/user/in")

    @app.route("/u/in/check", methods=["POST"])
    @app.route("/user/in/check", methods=["POST"])
    def check_sign_in_details():
        credentials = request.get_json()
        user_data = accounts_db.get(credentials.get("userid"))

        if not user_data: return jsonify({
            "status": 404,
            "msg": "User not found!"
        })

        if user_data["password"] != encrypt(credentials.get("password")):
            return jsonify({
                "status": 403,
                "msg": "Password not matched!"
            })

        session["userid"] = credentials.get("userid")

        return jsonify({"status": 200, "msg": "OK"})

    @app.route("/u/new/check", methods=["POST"])
    @app.route("/user/new/check", methods=["POST"])
    def check_sign_up_details():
        credentials = request.get_json()
        if accounts_db.get(credentials.get("userid")): return jsonify({
            "status": 403,
            "msg": "User ID already taken..."
        })
        
        accounts_db.put({
            "userid": credentials.get("userid", "NA"),
            "password": encrypt(credentials.get("password", "")),
            "articles": [],
            "data": {
                "name": credentials.get("name", "NA"),
                "mail": credentials.get("mail", "NA"),
                "img": "",
                "age": 0,
                "bio": ""
            },
            "permissions": []
        }, credentials.get("userid"))

        session["userid"] = credentials.get("userid")

        return jsonify({"status": 200, "msg": "OK"})
    
    @app.route("/users/get", methods=["POST"])
    def users_get():
        requested_users = request.get_json()
        data = []

        for user_id in requested_users:
            if not user_id: continue
            user_data = accounts_db.get(user_id)

            if not user_data: continue
            del user_data["password"]
            del user_data["userid"]
            if "key" in user_data: del user_data["key"]

            user_data["id"] = user_id
            data.append(user_data)

        return jsonify({"data": data, "status": 200, "msg": "OK"})

    @app.route("/dash")
    @app.route("/dashboard")
    @app.route("/u/dash")
    @app.route("/u/dashboard")
    @app.route("/user/dash")
    @app.route("/user/dashboard")
    def dashboard():
        if not is_logged_in(): return redirect("/user/in")
        user_data = accounts_db.get(session["userid"])
        
        del user_data["password"]
        del user_data["userid"]

        if "key" in user_data: del user_data["key"]

        user_data["id"] = session["userid"]
        user_data.update(user_data["data"])

        return f("user/dash/dash.html", **user_data)

    @app.route("/u/<user_id>")
    @app.route("/user/<user_id>")
    @app.route("/profile/<user_id>")
    @app.route("/user/profile/<user_id>")
    def user_profile(user_id: str):
        user_data = accounts_db.get(user_id)

        if not user_data: return redirect("/404")
        
        del user_data["password"]
        del user_data["userid"]

        if "key" in user_data: del user_data["key"]

        user_data["id"] = user_id
        user_data.update(user_data["data"])

        return f("user/dash/profile.html", **user_data)

    @app.route("/user/articles", methods=["POST"])
    def user_articles():
        requested_topics = request.get_json()
        data = {}

        for topic, quantity in requested_topics.items():
            topic_articles = accounts_db.get(topic)

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

