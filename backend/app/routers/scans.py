from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Finding
from app.auth.rbac import require_role
import xml.etree.ElementTree as ET

router = APIRouter(prefix="/scans", tags=["Scans"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🔐 ADMIN ONLY: upload scans
@router.post(
    "/upload",
    dependencies=[Depends(require_role(["admin"]))]
)
async def upload_scan(
    tool: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    content = await file.read()

    # Basic XML parsing (Nessus / OpenVAS style)
    root = ET.fromstring(content)

    count = 0
    for vuln in root.iter("ReportItem"):
        cve = vuln.attrib.get("cve", "NA")
        severity = vuln.attrib.get("severity", "Medium")

        finding = Finding(
            cve_id=cve,
            severity=severity,
            asset="uploaded-scan",
            tool=tool
        )
        db.add(finding)
        count += 1

    db.commit()
    return {
        "message": "Scan processed successfully",
        "findings_added": count
    }
