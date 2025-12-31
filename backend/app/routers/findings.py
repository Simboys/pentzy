from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import crud, schemas

router = APIRouter(prefix="/findings", tags=["Findings"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_finding(finding: schemas.FindingCreate, db: Session = Depends(get_db)):
    return crud.create_finding(db, finding)

@router.get("/")
def list_findings(db: Session = Depends(get_db)):
    return crud.get_findings(db)
