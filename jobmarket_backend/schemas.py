from pydantic import BaseModel
from datetime import date
from typing import Optional

# ✅ Schema for reading job data (Response Model)
class JobBase(BaseModel):
    company: str
    title: str
    salary: Optional[int] = None
    location: str
    job_type: str
    post_date: date
    job_link: str

# ✅ Schema for creating a job (Request Model)
class JobCreate(JobBase):
    pass  # Same as JobBase, but explicitly used for POST requests

# ✅ Schema for returning job data (Response Model)
class JobResponse(JobBase):
    id: int  # Includes the job ID in the response

    class Config:
        from_attributes = True  # Needed to convert SQLAlchemy models to Pydantic