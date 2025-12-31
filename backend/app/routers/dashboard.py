from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Finding
from app.auth.rbac import require_role

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🔐 ADMIN + ANALYST: dashboard access
@router.get(
    "/summary",
    dependencies=[Depends(require_role(["admin", "analyst"]))]
)
def summary(db: Session = Depends(get_db)):
    return {
        "total_findings": db.query(Finding).count(),
        "critical": db.query(Finding).filter(Finding.severity == "Critical").count(),
        "high": db.query(Finding).filter(Finding.severity == "High").count()
    }
