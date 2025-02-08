from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Update this with your actual PostgreSQL credentials
DATABASE_URL = "postgresql://postgres:ichab0d@localhost:5432/jobmarket"

# Create database engine
engine = create_engine(DATABASE_URL)

# Session to interact with the DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Define Job Model
class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, nullable=False)
    title = Column(String, nullable=False)
    salary = Column(Integer, nullable=True)
    location = Column(String, nullable=False)
    job_type = Column(String, nullable=False)
    post_date = Column(Date, nullable=False)

# Function to initialize the database
def init_db():
    Base.metadata.create_all(bind=engine)