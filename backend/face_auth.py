import face_recognition
import bcrypt
import os
import pickle
import cv2
import datetime

DATA_FILE = "known_faces/encodings.pkl"
MAX_FAILED_ATTEMPTS = 3
LOCK_DURATION_MINUTES = 5
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

    # ❗ Check if email already exists
    if email in known_data:
        return False, "User already registered", None

    new_encoding = encodings[0]

    # 🔴 NEW LOGIC: Check if face already registered
    for existing_email, user_data in known_data.items():
        existing_encoding = user_data["encoding"]

        match = face_recognition.compare_faces(
            [existing_encoding], new_encoding, tolerance=0.5
        )

        if match[0]:
            return False, f"This face is already registered with another account ({existing_email})", None

    # If no duplicate face found → continue registration
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    known_data[email] = {
        "password": hashed_password,
        "encoding": new_encoding,
        "failed_attempts": 0,
        "locked": False,
        "lock_time": None
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

    # 🔒 Lock Check
    if user.get("locked", False):
        lock_time = user.get("lock_time")

        if lock_time:
            elapsed_time = datetime.datetime.utcnow() - lock_time

            if elapsed_time.total_seconds() >= LOCK_DURATION_MINUTES * 60:
                user["locked"] = False
                user["failed_attempts"] = 0
                user["lock_time"] = None
                save_encodings(known_data)
            else:
                remaining_seconds = LOCK_DURATION_MINUTES * 60 - elapsed_time.total_seconds()
                remaining_minutes = int(remaining_seconds // 60) + 1
                return False, f"Account locked. Try again in {remaining_minutes} minute(s)", None
        else:
            return False, "Account is locked", None

    # 🔑 PASSWORD CHECK (VERY IMPORTANT)
    if not bcrypt.checkpw(password.encode("utf-8"), user["password"]):
        user["failed_attempts"] += 1

        if user["failed_attempts"] >= MAX_FAILED_ATTEMPTS:
            user["locked"] = True
            user["lock_time"] = datetime.datetime.utcnow()

        save_encodings(known_data)
        return False, "Incorrect password", None

    # 👤 FACE CHECK
    match = face_recognition.compare_faces(
        [user["encoding"]], encodings[0], tolerance=0.5
    )

    if not match[0]:
        user["failed_attempts"] += 1

        if user["failed_attempts"] >= MAX_FAILED_ATTEMPTS:
            user["locked"] = True
            user["lock_time"] = datetime.datetime.utcnow()

        save_encodings(known_data)
        return False, "Face not matched", None

    # ✅ SUCCESS
    user["failed_attempts"] = 0
    save_encodings(known_data)

    image_with_box = draw_face_box(rgb_image.copy(), face_locations)

    return True, "Login successful", image_with_box