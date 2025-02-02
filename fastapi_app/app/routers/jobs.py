from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import Job
from database import get_db

router = APIRouter()

@router.get("/jobs")
def get_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Job).offset(skip).limit(limit).all()