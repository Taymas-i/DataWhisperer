from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models import database_models

router = APIRouter()

@router.get("/health")
def check_health():
    return {"status": "Backend is running smoothly"}

@router.get("/data")
def get_all_data(db: Session = Depends(get_db)):
    # This queries the database for everything in the ProjectData table
    data = db.query(database_models.ProjectData).all()
    return data