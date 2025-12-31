from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import crud, schemas, models
from app.auth.rbac import require_role
from app.auth.deps import get_current_user
from app.audit import log_action

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
    dependencies=[Depends(require_role(["admin"]))],
)
def create_finding(
    finding: schemas.FindingCreate,
    db: Session = Depends(get_db),
):
    return crud.create_finding(db, finding)

# 🔐 ADMIN + ANALYST: view findings
@router.get(
    "/",
    dependencies=[Depends(require_role(["admin", "analyst"]))],
)
def list_findings(db: Session = Depends(get_db)):
    return crud.get_findings(db)

# 🔥 ADMIN ONLY: update finding status (Lifecycle)
@router.put(
    "/{finding_id}/status",
    dependencies=[Depends(require_role(["admin"]))],
)
def update_finding_status(
    finding_id: int,
    data: schemas.FindingUpdateStatus,
    request: Request,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    finding = (
        db.query(models.Finding)
        .filter(models.Finding.id == finding_id)
        .first()
    )

    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")

    old_status = finding.status
    finding.status = data.status
    db.commit()

    # 🧾 Audit log
    log_action(
        db=db,
        username=user["sub"],
        role=user["role"],
        action="UPDATE_FINDING_STATUS",
        resource=f"finding:{finding_id} {old_status}->{data.status}",
        ip=request.client.host if request.client else "unknown",
    )

    return {
        "message": "Finding status updated",
        "finding_id": finding_id,
        "old_status": old_status,
        "new_status": data.status,
    }

