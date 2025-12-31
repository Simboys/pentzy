from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import crud, schemas
from app.auth.rbac import require_role

router = APIRouter(prefix="/findings", tags=["Findings"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🔐 ADMIN ONLY: create finding
@router.post(
    "/",
    dependencies=[Depends(require_role(["admin"]))]
)
def create_finding(
    finding: schemas.FindingCreate,
    db: Session = Depends(get_db)
):
    return crud.create_finding(db, finding)

# 🔐 ADMIN + ANALYST: view findings
@router.get(
    "/",
    dependencies=[Depends(require_role(["admin", "analyst"]))]
)
def list_findings(db: Session = Depends(get_db)):
    return crud.get_findings(db)
