from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from ..database import get_db

router = APIRouter()

@router.get("/jobs")
def get_jobs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    # Define the raw SQL query
    query = text("""
        SELECT * FROM jobs
        OFFSET :skip
        LIMIT :limit
    """)
    
    # Execute the query with parameters
    result = db.execute(query, {"skip": skip, "limit": limit})
    
    # Fetch all rows and convert them to a list of dictionaries
    jobs = [dict(row) for row in result.mappings()]
    
    return jobs