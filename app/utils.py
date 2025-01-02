from passlib.context import CryptContext
from fastapi import HTTPException
from openai import OpenAI
import os

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def generate_interview_prep(job_title: str, job_description: str, resume: str):
    prompt = (
        f"I am preparing for an interview for a {job_title} position. "
        f"Here is the job description: {job_description}. "
        f"My resume is as follows: {resume}. "
        "What are some likely interview questions and how should I answer them?"
    )
    try:
        completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant specializing in assisting users with interview preparation"},
            {"role": "user", "content": prompt}
        ]
        )
        print(completion.choices[0].message.content)
        return {"questions_answers": completion.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
def cv_resume_review(resume: str, job_description: str):
    """
    Reviews a resume and provides suggestions for improvement based on a job description.

    Args:
        resume (str): The text of the user's resume.
        job_description (str): The job description for the desired position.

    Returns:
        dict: A dictionary containing feedback and recommendations for the resume.
    """
    prompt = (
        f"Review the following resume: {resume}. "
        f"Compare it to this job description: {job_description}. "
        "Provide detailed feedback on strengths, weaknesses, and areas for improvement. "
        "Suggest specific changes to align the resume with the job description, and identify any missing skills."
        "Point to specific parts of the resume that might need improvements to beat ATS and make corrections while referencing those parts"
    )
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional resume reviewer and career coach."},
                {"role": "user", "content": prompt}
            ]
        )
        return {"resume_feedback": completion.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

