from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import get_current_user
from pydantic import BaseModel
from typing import Optional
from app.utils import generate_interview_prep
from app.models import InterviewPrep
from app.database import get_db
from sqlalchemy.orm import Session


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

@router.post("/", response_model=InterviewPrepResponse)
def create_interview_prep(
    request: InterviewPrepRequest,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Generate interview questions and answers
    questions_answers = generate_interview_prep(request.job_title, request.job_description, request.resume)
    questions_answers_value = questions_answers.get("questions_answers", "")


    # Create a new interview prep record
    interview_prep = InterviewPrep(
        user_id=current_user.id,  # Assuming `current_user` contains the authenticated user's ID
        job_title=request.job_title,
        job_description=request.job_description,
        interview_date=request.interview_date,
        resume=request.resume,
        questions_answers=questions_answers_value,
    )

    db.add(interview_prep)
    db.commit()
    db.refresh(interview_prep)  # Retrieve the updated record

    return {
        "id": interview_prep.id,
        "job_title": interview_prep.job_title,
        "job_description": interview_prep.job_description,
        "interview_date": interview_prep.interview_date,
        "questions_answers": questions_answers_value,
    }

@router.get("/{id}", response_model=InterviewPrepResponse)
def get_interview_prep(
    id: int,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    interview_prep = db.query(InterviewPrep).filter(
        InterviewPrep.id == id,
        InterviewPrep.user_id == current_user.id  # Ensure the user owns the record
    ).first()

    if not interview_prep:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview prep not found")

    return {
        "id": interview_prep.id,
        "job_title": interview_prep.job_title,
        "job_description": interview_prep.job_description,
        "interview_date": interview_prep.interview_date,
        "questions_answers": interview_prep.questions_answers,
    }

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_interview_prep(
    id: int,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    interview_prep = db.query(InterviewPrep).filter(
        InterviewPrep.id == id,
        InterviewPrep.user_id == current_user.id  # Ensure the user owns the record
    ).first()

    if not interview_prep:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview prep not found")

    db.delete(interview_prep)
    db.commit()
    return
