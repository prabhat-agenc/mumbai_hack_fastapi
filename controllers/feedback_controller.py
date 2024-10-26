from fastapi import HTTPException
from llm_config import get_llm_session
from pymongo import MongoClient, DESCENDING
from langchain.schema import HumanMessage
from bson import ObjectId
from dotenv import load_dotenv
import os

import prompts.feedback_prompts as prompt

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

# Connect to database
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
feedback_collection = db["Feedback"]

user_type_collections = {
    "ServiceProvider": "serviceproviders",
    "ServiceSeeker": "serviceseekers",
    "Contractor": "contractors",
}

# Initialize LLM session
llm_session = get_llm_session()


def feedback_summary(user_id):
    try:
        user_data = db["authentications"].find_one({"_id": ObjectId(user_id)})

        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")

        user_type = user_data.get("userType")

        if user_type not in user_type_collections:
            raise HTTPException(status_code=400, detail="Invalid user type")

        summary_collection = db[user_type_collections[user_type]]

        # Fetch 10 most recent feedback entries for the specified user
        recent_feedbacks = (
            feedback_collection.find({"forUserID": ObjectId(user_id)})
            .sort("timestamp", DESCENDING)
            .limit(7)
        )

        # Extract 'feedbackText' attribute from each entry
        feedback_texts = [
            f"{i + 1}. {feedback.get('feedbackText', '')}"
            for i, feedback in enumerate(recent_feedbacks)
            if "feedbackText" in feedback
        ]

        # Format the prompt with collected feedback texts
        formatted_prompt = prompt.feedback_prompt.format(
            feedbacks="\n".join(feedback_texts)  # Joining feedback texts for the prompt
        )

        # Send formatted prompt to LLM
        message = HumanMessage(content=formatted_prompt)
        response = llm_session.invoke([message])
        feedback_summary_text = response.content

        # Store the summary in the user-specific collection
        summary_collection_update = summary_collection.update_one(
            {"authID": ObjectId(user_id)},
            {"$set": {"feedBackSummary": feedback_summary_text}},
            upsert=True,  # Create the document if it doesn't exist
        )
        print(summary_collection_update)

        return "success"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
