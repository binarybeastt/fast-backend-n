from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import get_current_user
from pydantic import BaseModel
from typing import Optional
from app.utils import generate_interview_prep

# Define a router instance
router = APIRouter()

# Pydantic models for request and response
class InterviewPrepRequest(BaseModel):
    job_title: str
    job_description: str
    interview_date: Optional[str] = None  # Optional, could use datetime instead
    resume: str  # Assume resume is a string, e.g., a URL or base64 encoded text

class InterviewPrepResponse(BaseModel):
    id: int
    job_title: str
    job_description: str
    interview_date: Optional[str] = None
    questions_answers: dict  # Store generated questions and answers

# In-memory storage (Replace with database interaction)
interview_data_store = {}
next_id = 1

@router.post("/", response_model=InterviewPrepResponse)
def create_interview_prep(request: InterviewPrepRequest, current_user: str = Depends(get_current_user)):
    global next_id

    # Use OpenAI API to generate interview questions and answers
    questions_answers = generate_interview_prep(request.job_title, request.job_description, request.resume)

    # Create and store interview prep data
    interview_prep = {
        "id": next_id,
        "job_title": request.job_title,
        "job_description": request.job_description,
        "interview_date": request.interview_date,
        "questions_answers": questions_answers,
    }

    interview_data_store[next_id] = interview_prep
    next_id += 1

    return interview_prep

@router.get("/{id}", response_model=InterviewPrepResponse)
def get_interview_prep(id: int, current_user: str = Depends(get_current_user)):
    interview_prep = interview_data_store.get(id)
    if not interview_prep:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview prep not found")
    
    return interview_prep

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_interview_prep(id: int, current_user: str = Depends(get_current_user)):
    if id not in interview_data_store:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview prep not found")
    
    del interview_data_store[id]
    return
