from sqlalchemy import Column, Integer, String, Text
from database import Base

class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True)
    job_title = Column(String)
    description = Column(Text)
    salary = Column(String)
    currency = Column(String)
    requirements = Column(Text)
    benefits = Column(Text)
    location = Column(String)
    business_name = Column(String)