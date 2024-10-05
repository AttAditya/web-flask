from modules.extensions import f
from flask import jsonify, redirect
from random import choice

def add_routes(app, dbs):
    ads_db = dbs["ads"]

    @app.route("/ads.txt")
    def google_ads():
        return f("ads.txt")

    @app.route("/TAC")
    @app.route("/policy")
    def TAC():
        return f("misc/TAC.html")

    @app.route("/credits")
    def twt_credits():
        return f("misc/credits.html")

    @app.route("/policy/ads")
    def ad_policy():
        return f("misc/advertise.html")
    
    @app.route("/ad/get")
    def ad_img():
        ads_index = ads_db.get("INDEX")
        if not ads_index or not ads_index["ids"]: return jsonify({
            "status": 200,
            "msg": "OK",
            "link": "/",
            "img": "/res/logo.png"
        })

        ad_index = choice(ads_index["ids"])
        ad_data = ads_db.get(ad_index)
        ad_data["count"] += 1

        ads_db.put(ad_data, ad_index)

        return jsonify({
            "status": 200,
            "msg": "OK",
            "link": ad_data["link"],
            "img": ad_data["img"],
            "text": ad_data["text"]
        })

    @app.route("/ad/<ad_id>/analytics")
    def ad_analytics(ad_id: str):
        ad_meta_data = ads_db.get(ad_id)
        if not ad_meta_data: return redirect("/404")

        return jsonify(ad_meta_data)

