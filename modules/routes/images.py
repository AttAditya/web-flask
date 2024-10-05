from flask import request, jsonify, send_file
from uuid import uuid1
from io import BytesIO

def add_routes(app, dbs):
    picture_dr = dbs["picture_drive"]

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
