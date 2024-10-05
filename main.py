from __future__ import annotations
from os import environ
from os.path import isfile

def f(path: str, *, root: str="web/", tokenizer: callable=lambda s: f"[[{s}]]", **replace) -> str:
	"""
	Checks if a file exists and if does returns its contents or else an empty string if not.
	"""

	fpath = root + path
	
	if not isfile(fpath): return ""
	
	data = ""
	with open(fpath, "r") as file:
		data = file.read()
		file.close()
	
	if not replace: return data

	for rkey in replace:
		data = data.replace(tokenizer(rkey), str(replace[rkey]))
	
	return data

def encrypt(data: str) -> str:
	"""
	Encrypts data
	"""

	cipher_num = "".join([str(ord(ch) * len(data) * i) for i, ch in enumerate(data)])
	cipher = ""

	if len(cipher_num) % 2 == 1: cipher_num += "0"

	buffer = ""
	for i, c in enumerate(cipher_num):
		if i % 2 == 1: buffer = c; continue
		cipher += chr((int(buffer + c) % 65) + 65)
	
	return cipher[::-2] + cipher[1::2]

import logging
from flask import Flask, session, request, jsonify, send_file, redirect
from uuid import uuid1
from datetime import datetime, timezone
from io import BytesIO
from base64 import b64decode
from random import choice

logging.getLogger("werkzeug").setLevel(logging.ERROR)

app = Flask("TWTDB", static_folder="res", static_url_path="/res")
app.secret_key = environ.get("SECRET", "this_is_a_test_key_that_should_not_be_in_deployment")

import deta as deta_sh

deta = deta_sh.Deta()
content_db = deta.Base("Content")
tags_db = deta.Base("Tags")
content_dr = deta.Drive("Content-Drive")
thumbnails_dr = deta.Drive("Thumbnails")
picture_dr = deta.Drive("Pictures")
accounts_db = deta.Base("Accounts")
ads_db = deta.Base("Ads")
analytics_db = deta.Base("Analytics")
errors_db = deta.Base("Errors")

def is_logged_in() -> bool:
	"""
	Check if user is logged in...
	"""

	if "userid" not in session: return False
	if not accounts_db.get(session.get("userid")): return False

	return True

@app.errorhandler(404)
@app.route("/404")
def err404(*_, **__):
	return jsonify(["404 - Page Not Found"])

@app.route("/")
def home():
	return f("index.html")

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

@app.route("/upload/image", methods=["POST"])
def upload_image() -> str:
	if "file" not in request.files: return jsonify({
		"status": 418,
		"msg": "I'm a teapot."
	})

	file = request.files["file"]
	file_ext = file.mimetype.split("/")[1].lower()

	image_id = uuid1().hex

	image_name = f"{image_id}.{file_ext}"
	image_link = f"/i/{image_name}"

	picture_dr.put(image_name, file.stream)

	data = jsonify({
		"name": image_name,
		"location": image_link
	})

	return data

@app.route("/i/<image_name>")
@app.route("/image/<image_name>")
def content_image(image_name: str):
	picture_file = picture_dr.get(image_name)
	
	if not picture_file: return "Not Found"
	picture_stream = picture_file.read()

	return send_file(BytesIO(picture_stream), download_name=image_name)

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

if __name__ == "__main__":
	app.run("0.0.0.0", 8000)

