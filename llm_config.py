from langchain_aws import ChatBedrock
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def get_llm_session(model_id: str = "meta.llama3-70b-instruct-v1:0"):
    # Configure AWS Bedrock for LLM inference
    bedrock_chat = ChatBedrock(
        model_id=model_id,
        model_kwargs={
            "max_tokens": 1500,
            "temperature": 0.7,
            "top_p": 0.9,
        },
        region_name=os.getenv("AWS_DEFAULT_REGION"),
    )
    
    return bedrock_chat