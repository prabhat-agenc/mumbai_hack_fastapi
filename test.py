# from fastapi import HTTPException
# from llm_config import get_llm_session
from pymongo import MongoClient, DESCENDING
# from langchain.schema import HumanMessage
from bson import ObjectId
from dotenv import load_dotenv
import os

# import prompts.feedback_prompts as prompt

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

# Connect to database
client = MongoClient(MONGO_URI)
db = client["test"]
feedback_collection = db["Feedback"]

collections = db.list_collection_names()
print("Collections in the database:", collections)

print(db)
user_data = db["authentications"].find_one({"_id": ObjectId("671c49b735101beec3eaf29d")})
print(user_data)