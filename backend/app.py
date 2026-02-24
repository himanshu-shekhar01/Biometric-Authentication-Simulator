from flask import Flask, request, jsonify
import base64
import numpy as np
import cv2
from flask_cors import CORS
from face_auth import register_face, verify_face
import jwt
import datetime
from functools import wraps

print("🔥 THIS IS THE ACTIVE BACKEND FILE")

app = Flask(__name__)
app.config["SECRET_KEY"] = "my_ultra_secure_very_long_secret_key_2026_auth_project"
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


@app.route("/")
def home():
    return jsonify({"message": "Backend Running Successfully!"})


# =========================
# Helper Function
# =========================
def process_base64_image(image):
    header, encoded = image.split(",", 1)
    img_bytes = base64.b64decode(encoded)
    nparr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return rgb_img


def convert_image_to_base64(rgb_image):
    bgr_img = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
    _, buffer = cv2.imencode(".jpg", bgr_img)
    img_base64 = base64.b64encode(buffer).decode("utf-8")
    return f"data:image/jpeg;base64,{img_base64}"


# =========================
# REGISTER ROUTE
# =========================
@app.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json(force=True)
        email = data.get("email")
        password = data.get("password")
        image = data.get("image")

        if not image:
            return jsonify({"success": False, "status": "No Image Provided"})

        rgb_img = process_base64_image(image)

        success, message, image_with_box = register_face(
            email, password, rgb_img
        )

        img_base64 = convert_image_to_base64(image_with_box) if image_with_box is not None else None

        return jsonify({
            "success": success,
            "status": message,
            "image": img_base64
        })

    except Exception as e:
        return jsonify({"error": str(e)})


# =========================
# LOGIN ROUTE
# =========================
@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json(force=True)
        email = data.get("email")
        password = data.get("password")
        image = data.get("image")

        if not image:
            return jsonify({"success": False, "status": "No Image Provided"})

        rgb_img = process_base64_image(image)

        success, message, image_with_box = verify_face(
            email, password, rgb_img
        )

        img_base64 = convert_image_to_base64(image_with_box) if image_with_box is not None else None

        if success:
            token = jwt.encode({
                "email": email,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }, app.config["SECRET_KEY"], algorithm="HS256")

            return jsonify({
            "success": True,
            "status": message,
            "token": token,
            "image": img_base64
    })
        else:
            return jsonify({
            "success": False,
            "status": message,
            "image": img_base64
    })

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)