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
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
        )
        return {"questions_answers": completion.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
