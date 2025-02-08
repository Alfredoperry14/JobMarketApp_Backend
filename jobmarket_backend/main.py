from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, init_db, Job  # Import database setup

app = FastAPI()

# Initialize database (only needed once)
init_db()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ 1. Fetch all job listings
@app.get("/jobs")
def get_jobs(db: Session = Depends(get_db)):
    jobs = db.query(Job).all()
    return jobs

# ✅ 2. Add a new job listing
@app.post("/jobs")
def create_job(job: Job, db: Session = Depends(get_db)):
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

# ✅ 3. Fetch a job by ID
@app.get("/jobs/{job_id}")
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job