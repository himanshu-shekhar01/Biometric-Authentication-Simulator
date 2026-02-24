import face_recognition
import bcrypt
import os
import pickle
import cv2

DATA_FILE = "known_faces/encodings.pkl"
MAX_FAILED_ATTEMPTS = 3

os.makedirs("known_faces", exist_ok=True)


# =========================
# Load Encodings
# =========================
def load_encodings():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "rb") as f:
            return pickle.load(f)
    return {}


# =========================
# Save Encodings
# =========================
def save_encodings(data):
    with open(DATA_FILE, "wb") as f:
        pickle.dump(data, f)


# =========================
# Draw Face Box
# =========================
def draw_face_box(image, face_locations):
    for (top, right, bottom, left) in face_locations:
        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
    return image


# =========================
# REGISTER
# =========================
def register_face(email, password, rgb_image):
    face_locations = face_recognition.face_locations(rgb_image)
    encodings = face_recognition.face_encodings(rgb_image)

    if len(encodings) == 0:
        return False, "No face found", None

    if len(encodings) > 1:
        return False, "Multiple faces detected", None

    known_data = load_encodings()

    if email in known_data:
        return False, "User already registered", None

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    known_data[email] = {
        "password": hashed_password,
        "encoding": encodings[0],
        "failed_attempts": 0,
        "locked": False
    }

    save_encodings(known_data)

    image_with_box = draw_face_box(rgb_image.copy(), face_locations)

    return True, "Face registered successfully", image_with_box


# =========================
# LOGIN
# =========================
def verify_face(email, password, rgb_image):
    face_locations = face_recognition.face_locations(rgb_image)
    encodings = face_recognition.face_encodings(rgb_image)

    if len(encodings) == 0:
        return False, "No face found", None

    if len(encodings) > 1:
        return False, "Multiple faces detected", None

    known_data = load_encodings()

    if email not in known_data:
        return False, "User not registered", None

    user = known_data[email]

    if user["locked"]:
        return False, "Account is locked", None

    # Check password
    if not bcrypt.checkpw(password.encode("utf-8"), user["password"]):
        user["failed_attempts"] += 1
        if user["failed_attempts"] >= MAX_FAILED_ATTEMPTS:
            user["locked"] = True
        save_encodings(known_data)
        return False, "Incorrect password", None

    # Check face match
    match = face_recognition.compare_faces(
        [user["encoding"]], encodings[0], tolerance=0.5
    )

    if not match[0]:
        user["failed_attempts"] += 1
        if user["failed_attempts"] >= MAX_FAILED_ATTEMPTS:
            user["locked"] = True
        save_encodings(known_data)
        return False, "Face not matched", None

    # Successful login
    user["failed_attempts"] = 0
    save_encodings(known_data)

    image_with_box = draw_face_box(rgb_image.copy(), face_locations)

    return True, "Login successful", image_with_box