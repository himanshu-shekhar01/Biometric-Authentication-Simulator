# Multi-Modal Biometric Authentication System  
### Face Recognition + Fingerprint Authentication  

A secure biometric authentication system built using **Flask (Python)** and **React**, implementing face recognition and fingerprint-based authentication with additional security features like password hashing, JWT authentication, and account lock mechanism.

---

## Project Overview

This project implements a **multi-modal biometric authentication system** that enhances security by combining:

- 👤 Face Recognition
- 🖐 Fingerprint Authentication (Conceptual / Extendable)
- 🔐 Hashed Password Authentication
- 🛡 JWT-Based Secure Sessions
- 🚫 Failed Attempt Lock System

The system avoids storing raw biometric images and instead stores secure biometric templates.

---

## Technologies Used

### 🔹 Backend
- Python 3.10
- Flask
- OpenCV
- face_recognition (dlib-based model)
- bcrypt (Password hashing)
- PyJWT (Token authentication)
- Flask-CORS
- Pickle (Local storage for templates)

### 🔹 Frontend
- React.js
- Webcam API
- Axios (API communication)
- Tailwind CSS (UI styling)

---

## 🏗 System Architecture
User
↓
React Frontend (Camera Capture)
↓
Flask Backend API
↓
Face Recognition Engine
↓
Template Storage (encodings.pkl)
↓
JWT Authentication Response


---

## 👤 Face Recognition Workflow

1. User captures face using webcam.
2. Image is sent as Base64 to backend.
3. Backend converts image using OpenCV.
4. Face is detected using `face_recognition`.
5. 128-Dimensional Face Encoding is generated.
6. Encoding is compared using Euclidean distance.
7. If distance < threshold → Authentication Success.

### 🔎 Important Concept:
We store only **face encodings (numerical vectors)**, not raw images.

---

## 🖐 Fingerprint Authentication (Concept)

Fingerprint recognition works by:

- Extracting unique ridge patterns
- Detecting minutiae points (ridge endings & bifurcations)
- Creating a biometric template
- Matching template during login

Currently implemented conceptually and can be extended using hardware sensor integration.

---

## 🔐 Security Features

- Password hashing using bcrypt
- JWT token authentication
- Maximum 3 failed login attempts
- 5-minute account lock system
- No raw image storage
- CORS protection enabled

---

## 📁 Project Structure


---

## 🚀 How To Run The Project

### 🔹 1️⃣ Backend Setup

```bash
cd backend
python3.10 -m venv venv
source venv/bin/activate   # Mac/Linux
# OR
venv\Scripts\activate      # Windows

pip install -r requirements.txt
python app.py
```
Server will run on:
http://127.0.0.1:5000

# Frontend Setup

Open new terminal:
```
cd frontend
npm install
npm start
```

Frontend will run on:

http://localhost:3000

