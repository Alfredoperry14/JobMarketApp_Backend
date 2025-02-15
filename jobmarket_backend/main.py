from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from jobmarket_backend.database import SessionLocal, init_db, Job
from jobmarket_backend import schemas
from config import API_TOKEN  # Import the token

app = FastAPI()

# Initialize database (only needed once)
init_db()

@app.get("/")
def root():
    return {"message": "FastAPI is running!"}

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Token dependency using the imported token
def verify_token(x_token: str = Header(...)):
    if x_token != API_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token")

# 1. Fetch all job listings (with token verification)
@app.get("/jobs", response_model=list[schemas.JobResponse], dependencies=[Depends(verify_token)])
def get_jobs(db: Session = Depends(get_db)):
    jobs = db.query(Job).all()
    return jobs

# 2. Add a new job listing (with token verification)
@app.post("/jobs", response_model=schemas.JobResponse, dependencies=[Depends(verify_token)])
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db)):
    db_job = Job(**job.model_dump())  # Convert Pydantic model to dictionary
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

# 3. Fetch a job by ID (with token verification)
@app.get("/jobs/{job_id}", response_model=schemas.JobResponse, dependencies=[Depends(verify_token)])
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job