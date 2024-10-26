from fastapi import APIRouter, HTTPException, Query
from controllers.feedback_controller import *

router = APIRouter()

# Generate content for idea provided
@router.get("/feedback-summary", response_model=str)
async def feedback_summary_route(user_id: str = Query(...)):
    return feedback_summary(user_id)