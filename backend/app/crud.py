from sqlalchemy.orm import Session
from app import models, schemas

def create_finding(db: Session, finding: schemas.FindingCreate):
    db_finding = models.Finding(**finding.dict())
    db.add(db_finding)
    db.commit()
    db.refresh(db_finding)
    return db_finding

def get_findings(db: Session):
    return db.query(models.Finding).all()
