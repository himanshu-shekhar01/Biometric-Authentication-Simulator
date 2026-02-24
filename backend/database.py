from pymongo import MongoClient

MONGO_URI = "mongodb+srv://triund89_db_user:triund21@cluster0.vsz8xi1.mongodb.net/?appName=Cluster0"

client = MongoClient(MONGO_URI)

db = client["biometric_auth"]
users_collection = db["users"]

print("✅ Connected to MongoDB Atlas")