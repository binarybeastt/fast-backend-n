# app/models.py
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    hashed_password = Column(String)

class InterviewPrep(Base):
    __tablename__ = "interview_preps"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Foreign key to users table
    job_title = Column(String, nullable=False)
    job_description = Column(Text, nullable=False)
    interview_date = Column(DateTime, nullable=True)
    resume = Column(Text, nullable=False)
    questions_answers = Column(Text, nullable=False)  # Store as JSON string

    user = relationship("User")  # Assuming `User` is the user model

class ResumeReview(Base):
    __tablename__ = "resume_reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Foreign key to users table
    resume = Column(Text, nullable=False)
    job_description = Column(Text, nullable=False)
    resume_review = Column(Text, nullable=False)  # Store as JSON string

    user = relationship("User")  # Assuming `User` is the user model