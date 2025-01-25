import logging
from fastapi import FastAPI, Depends
from app.database import engine
from app.models import Base
from app.routes import auth, interview, resume_review  # Import the routes
from app.dependencies import get_current_user  # Import the dependency
from fastapi.middleware.cors import CORSMiddleware
# from azure.monitor.opentelemetry import configure_azure_monitor

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://localhost:3000",
                   "https://nextjs-frontend-git-deji-binarybeastts-projects.vercel.app",
                   "https://nextjs-frontend-pi.vercel.app"], 
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"]
)

Base.metadata.create_all(bind=engine)

# Include authentication routes
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(interview.router, prefix="/interview-prep", tags=["interview-prep"], include_in_schema=True)
app.include_router(resume_review.router, prefix="/resume-review", tags=["resume-review"])

# Example of a protected route
@app.get("/protected-route/")
def read_protected_route(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello, {current_user}! You are authenticated."}
