from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import get_current_user
from pydantic import BaseModel
from typing import Optional
from app.utils import cv_resume_review
from app.models import ResumeReview
from app.database import get_db
from sqlalchemy.orm import Session
from datetime import datetime

# Define a router instance
router = APIRouter()

# Pydantic models for request and response
class ResumeReviewRequest(BaseModel):
    resume: str  # Assume resume is a string, e.g., a URL or base64 encoded text
    job_description: str

class ResumeReviewResponse(BaseModel):
    id: int
    resume: str
    job_description: str
    resume_review: str # Store generated resume review

@router.post("/", response_model=ResumeReviewResponse)
async def create_resume_review(
    request: ResumeReviewRequest,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Generate resume review
    resume_review = cv_resume_review(request.resume, request.job_description)
    resume_review_value = resume_review.get("resume_feedback", "")

    # Create a new resume review record
    resume_review = ResumeReview(
        user_id=current_user.id,  # Assuming `current_user` contains the authenticated user's ID
        resume=request.resume,
        job_description=request.job_description,
        resume_review=resume_review_value,  # Store the string
    )

    db.add(resume_review)
    db.commit()
    db.refresh(resume_review)

    return {
        "id": resume_review.id,
        "resume": resume_review.resume,
        "job_description": resume_review.job_description,
        "resume_review": resume_review_value,
    }
    